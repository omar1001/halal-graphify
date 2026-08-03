# re-export manifest helpers from detect for backwards compatibility
from halal_graphify.detect import save_manifest, load_manifest, detect_incremental

__all__ = ["save_manifest", "load_manifest", "detect_incremental"]
