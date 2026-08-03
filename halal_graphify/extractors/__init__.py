"""Per-language extractors, incrementally migrated out of halal_graphify/extract.py.

Dispatch still flows through halal_graphify.extract (the facade re-exports every
moved name), so importing from halal_graphify.extract keeps working unchanged.
LANGUAGE_EXTRACTORS is the registry seed; wiring dispatch through it is a
later, separate step. See MIGRATION.md for how to port another language.
"""
from __future__ import annotations

from pathlib import Path
from typing import Callable

from halal_graphify.extractors.apex import extract_apex
from halal_graphify.extractors.bash import extract_bash
from halal_graphify.extractors.blade import extract_blade
from halal_graphify.extractors.dart import extract_dart
from halal_graphify.extractors.dm import extract_dm, extract_dmf, extract_dmi, extract_dmm
from halal_graphify.extractors.elixir import extract_elixir
from halal_graphify.extractors.fortran import extract_fortran
from halal_graphify.extractors.go import extract_go
from halal_graphify.extractors.json_config import extract_json
from halal_graphify.extractors.julia import extract_julia
from halal_graphify.extractors.markdown import extract_markdown
from halal_graphify.extractors.objc import extract_objc
from halal_graphify.extractors.pascal import extract_pascal
from halal_graphify.extractors.pascal_forms import extract_delphi_form, extract_lazarus_form
from halal_graphify.extractors.powershell import extract_powershell, extract_powershell_manifest
from halal_graphify.extractors.razor import extract_razor
from halal_graphify.extractors.rust import extract_rust
from halal_graphify.extractors.sln import extract_sln
from halal_graphify.extractors.sql import extract_sql
from halal_graphify.extractors.terraform import extract_terraform
from halal_graphify.extractors.verilog import extract_verilog
from halal_graphify.extractors.zig import extract_zig

LANGUAGE_EXTRACTORS: dict[str, Callable[[Path], dict]] = {
    "apex": extract_apex,
    "bash": extract_bash,
    "blade": extract_blade,
    "dart": extract_dart,
    "delphi_form": extract_delphi_form,
    "dm": extract_dm,
    "dmf": extract_dmf,
    "dmi": extract_dmi,
    "dmm": extract_dmm,
    "elixir": extract_elixir,
    "fortran": extract_fortran,
    "go": extract_go,
    "json": extract_json,
    "julia": extract_julia,
    "lazarus_form": extract_lazarus_form,
    "markdown": extract_markdown,
    "objc": extract_objc,
    "pascal": extract_pascal,
    "powershell": extract_powershell,
    "powershell_manifest": extract_powershell_manifest,
    "razor": extract_razor,
    "rust": extract_rust,
    "sln": extract_sln,
    "sql": extract_sql,
    "terraform": extract_terraform,
    "verilog": extract_verilog,
    "zig": extract_zig,
}
