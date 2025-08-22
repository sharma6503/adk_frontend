import time
import functools
import inspect
from typing import Any, Callable, Dict, Optional, Tuple
import uuid

from ddtrace import tracer
try:
    from ddtrace.llmobs import LLMObs
except Exception:
    LLMObs = None

# ---------- DEFAULTS ----------
DEFAULT_SERVICE = "adk-agent"
DEFAULT_COMPONENT = "agent"
DEFAULT_TOOL_CONTEXT_NAMES = ("tool_context", "context", "ctx")
# ---------------------------------------------------------------------


def _try_get_tiktoken_encoder(model: Optional[str] = None):
    try:
        import tiktoken
    except Exception:
        return None

    try:
        if model:
            try:
                return tiktoken.encoding_for_model(model)
            except Exception:
                return tiktoken.get_encoding("cl100k_base")
        return tiktoken.get_encoding("cl100k_base")
    except Exception:
        return None


def _estimate_tokens_from_text(text: str, model: Optional[str] = None) -> int:
    if not text:
        return 0
    enc = _try_get_tiktoken_encoder(model)
    if enc is not None:
        try:
            return len(enc.encode(text))
        except Exception:
            pass
    return (len(text) + 3) // 4


def _is_intlike(x: Any) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


def _extract_tokens_from_usage(usage_obj) -> Tuple[Optional[int], Optional[int]]:
    try:
        if usage_obj is None:
            return None, None
        if isinstance(usage_obj, dict):
            in_t = usage_obj.get("input_tokens") or usage_obj.get("prompt_tokens") \
                   or usage_obj.get("prompt_token_count") or usage_obj.get("input_token_count")
            out_t = usage_obj.get("output_tokens") or usage_obj.get("completion_tokens") \
                    or usage_obj.get("output_token_count")
            try:
                in_t = int(in_t) if in_t is not None else None
            except Exception:
                in_t = None
            try:
                out_t = int(out_t) if out_t is not None else None
            except Exception:
                out_t = None
            return in_t, out_t

        for a in ("input_tokens", "prompt_tokens", "prompt_token_count", "input_token_count"):
            if hasattr(usage_obj, a):
                val = getattr(usage_obj, a)
                if _is_intlike(val):
                    in_t = int(val)
                    break
        else:
            in_t = None

        for a in ("output_tokens", "completion_tokens", "output_token_count"):
            if hasattr(usage_obj, a):
                val = getattr(usage_obj, a)
                if _is_intlike(val):
                    out_t = int(val)
                    break
        else:
            out_t = None

        return in_t, out_t
    except Exception:
        return None, None


def _extract_tokens_from_obj(
    obj: Any,
    model: Optional[str] = None,
    input_text: Optional[str] = None
) -> Tuple[Optional[int], Optional[int]]:

    try:
        if obj is None:
            return (_estimate_tokens_from_text(input_text, model), None) if input_text else (None, None)

        if isinstance(obj, dict):
            for usage_key in ("usage", "token_usage", "usage_info"):
                if usage_key in obj:
                    return _extract_tokens_from_usage(obj[usage_key])

        for attr in ("usage", "token_usage", "usage_info", "model_response"):
            if hasattr(obj, attr):
                return _extract_tokens_from_usage(getattr(obj, attr))
    except Exception:
        pass

    def _collect_texts_from_response(o, depth=0):
        if depth > 6 or o is None:
            return []
        texts = []
        try:
            if isinstance(o, dict):
                if "candidates" in o and isinstance(o["candidates"], (list, tuple)):
                    for c in o["candidates"]:
                        val = c.get("content") if isinstance(c, dict) else getattr(c, "content", None)
                        if isinstance(val, str):
                            texts.append(val)
                for key in ("response", "model_response", "output", "text", "message", "content"):
                    if key in o:
                        texts.extend(_collect_texts_from_response(o[key], depth + 1))
                for v in o.values():
                    texts.extend(_collect_texts_from_response(v, depth + 1))
            elif isinstance(o, (list, tuple)):
                for item in o:
                    texts.extend(_collect_texts_from_response(item, depth + 1))
            else:
                for attr in ("candidates", "response", "model_response", "output", "text", "message", "content"):
                    if hasattr(o, attr):
                        texts.extend(_collect_texts_from_response(getattr(o, attr), depth + 1))
                if hasattr(o, "__dict__"):
                    for v in vars(o).values():
                        texts.extend(_collect_texts_from_response(v, depth + 1))
        except Exception:
            pass
        return texts

    try:
        texts = _collect_texts_from_response(obj)
        str_texts = [t for t in texts if isinstance(t, str) and t.strip()]
        if str_texts:
            longest = max(str_texts, key=len)
            return (
                _estimate_tokens_from_text(input_text, model) if input_text else None,
                _estimate_tokens_from_text(longest, model),
            )
    except Exception:
        pass

    return (_estimate_tokens_from_text(input_text, model), None) if input_text else (None, None)


def _get_input_preview(args, kwargs) -> Optional[str]:
    try:
        for candidate in ("prompt", "query", "input", "text"):
            if candidate in kwargs and isinstance(kwargs[candidate], str):
                s = kwargs[candidate]
                return s if len(s) < 2000 else s[:2000] + "..."
        if args and isinstance(args[0], str):
            s = args[0]
            return s if len(s) < 2000 else s[:2000] + "..."
    except Exception:
        return None
    return None


def llm_obs(
    name: Optional[str] = None,
    component_type: str = DEFAULT_COMPONENT,
    service: str = DEFAULT_SERVICE,
    tool_context_names: Tuple[str, ...] = DEFAULT_TOOL_CONTEXT_NAMES,
    model: Optional[str] = None,
    cost_per_1k_input: Optional[float] = None,
    cost_per_1k_output: Optional[float] = None,
    cost_fn: Optional[Callable[[Optional[int], Optional[int]], float]] = None,
    extra_tags: Optional[Dict[str, Any]] = None,
):
    def _decorator(target):
        span_name = f"{component_type}.{name or getattr(target, '__name__', 'call')}".lower()

        if inspect.isclass(target):
            orig_cls = target
            class Wrapped(orig_cls): pass
            common_entrypoints = ("__call__", "run", "execute", "run_agent", "handle", "handle_request")
            for mname in common_entrypoints:
                if hasattr(orig_cls, mname):
                    orig_method = getattr(orig_cls, mname)
                    def make_wrapped_method(orig_m):
                        @functools.wraps(orig_m)
                        def wrapped_method(self, *args, **kwargs):
                            return _wrap_call(functools.partial(orig_m, self), args, kwargs)
                        return wrapped_method
                    setattr(Wrapped, mname, make_wrapped_method(orig_method))
            return Wrapped

        @functools.wraps(target)
        def wrapper(*args, **kwargs):
            return _wrap_call(target, args, kwargs)

        def _wrap_call(func: Callable, f_args: tuple, f_kwargs: dict):
            start = time.time()
            try:
                span = tracer.trace(span_name, service=service)
            except Exception:
                span = None

            inputs_preview = _get_input_preview(f_args, f_kwargs)
            if span and inputs_preview:
                span.set_tag("llm.input_preview", inputs_preview)

            exc, result = None, None
            try:
                result = func(*f_args, **f_kwargs)
                return result
            except Exception as e:
                exc = e
                if span:
                    span.set_tag("error", True)
                    span.set_tag("error.msg", str(e))
                raise
            finally:
                end = time.time()
                duration_s = end - start
                try:
                    input_tokens, output_tokens = _extract_tokens_from_obj(result, model=model, input_text=inputs_preview)
                except Exception:
                    input_tokens, output_tokens = None, None

                total_tokens = (input_tokens or 0) + (output_tokens or 0) if (input_tokens or output_tokens) else None

                cost = None
                try:
                    if cost_fn:
                        cost = cost_fn(input_tokens, output_tokens)
                    else:
                        cost = 0.0
                        if input_tokens and cost_per_1k_input:
                            cost += (input_tokens / 1000.0) * cost_per_1k_input
                        if output_tokens and cost_per_1k_output:
                            cost += (output_tokens / 1000.0) * cost_per_1k_output
                        if cost == 0.0:
                            cost = None
                except Exception:
                    cost = None

                tags = {
                    "component.type": component_type,
                    "component.name": name or getattr(func, "__name__", "call"),
                    "duration_s": round(duration_s, 6),
                    "has_error": bool(exc is not None),
                }
                if input_tokens is not None: tags["input_tokens"] = int(input_tokens)
                if output_tokens is not None: tags["output_tokens"] = int(output_tokens)
                if total_tokens is not None: tags["total_tokens"] = int(total_tokens)
                if cost is not None: tags["llm_cost_usd"] = float(cost)
                if model: tags["model"] = model
                if extra_tags: tags.update(extra_tags)

                if span:
                    for k, v in tags.items():
                        span.set_tag(k, v)

                try:
                    annotate_payload = {
                        "inputs": {"preview": inputs_preview} if inputs_preview else None,
                        "outputs": {"preview": str(result)[:2000] + "..." if result and len(str(result)) > 2000 else result},
                        "tags": tags,
                        "metrics": {k: v for k, v in tags.items() if isinstance(v, (int, float))},
                        "metadata": {
                            "run_id": str(uuid.uuid4()),
                            "timestamp": time.time(),
                            "component_type": component_type,
                        }
                    }
                    annotate_payload = {k: v for k, v in annotate_payload.items() if v is not None}
                    if LLMObs and hasattr(LLMObs, "annotate"):
                        LLMObs.annotate(**annotate_payload)

                    if span:
                        if input_tokens is not None: span.set_metric("input_tokens", int(input_tokens))
                        if output_tokens is not None: span.set_metric("output_tokens", int(output_tokens))
                        if cost is not None:
                            span.set_metric("llm_cost_usd", float(cost))
                            span.set_metric("total_cost", float(cost))
                except Exception:
                    pass

                if span:
                    span.finish()

        wrapper._llm_obs_span_name = span_name
        wrapper._llm_obs_component_type = component_type
        return wrapper

    if callable(name):
        return llm_obs()(name)

    return _decorator
