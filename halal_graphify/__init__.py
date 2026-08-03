"""halal-graphify - extract · build · cluster · analyze · report."""


def __getattr__(name):
    # Lazy imports so `halal-graphify install` works before heavy deps are in place.
    _map = {
        "extract": ("halal_graphify.extract", "extract"),
        "collect_files": ("halal_graphify.extract", "collect_files"),
        "build_from_json": ("halal_graphify.build", "build_from_json"),
        "cluster": ("halal_graphify.cluster", "cluster"),
        "score_all": ("halal_graphify.cluster", "score_all"),
        "cohesion_score": ("halal_graphify.cluster", "cohesion_score"),
        "hub_nodes": ("halal_graphify.analyze", "hub_nodes"),
        "surprising_connections": ("halal_graphify.analyze", "surprising_connections"),
        "suggest_questions": ("halal_graphify.analyze", "suggest_questions"),
        "generate": ("halal_graphify.report", "generate"),
        "to_json": ("halal_graphify.export", "to_json"),
        "to_html": ("halal_graphify.export", "to_html"),
        "to_svg": ("halal_graphify.export", "to_svg"),
        "to_canvas": ("halal_graphify.export", "to_canvas"),
        "to_wiki": ("halal_graphify.wiki", "to_wiki"),
        "reflect": ("halal_graphify.reflect", "reflect"),
        "save_query_result": ("halal_graphify.ingest", "save_query_result"),
    }
    if name in _map:
        import importlib
        mod_name, attr = _map[name]
        mod = importlib.import_module(mod_name)
        return getattr(mod, attr)
    raise AttributeError(f"module 'halal-graphify' has no attribute {name!r}")
