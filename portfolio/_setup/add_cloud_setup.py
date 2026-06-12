# -*- coding: utf-8 -*-
"""
يحقن خلية «إعداد التشغيل» (Colab/Kaggle/محلي) في بداية كل نوتبوك بالبورتفوليو.
- idempotent: ما بيكرّرش الحقن لو الخلية موجودة.
- بيحافظ على مخرجات النوتبوكات الحالية (مش بيعيد تنفيذها).
- بيكتشف مكتبات كل مشروع تلقائياً من الـ imports.
التشغيل:  python portfolio/_setup/add_cloud_setup.py
"""
import json, os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
PORTFOLIO = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(PORTFOLIO, "_datagen"))
from nbtools import cloud_setup_sources, SETUP_SENTINEL   # noqa: E402

# مكتبة (كما تُستورد) -> اسم pip (لو مختلف)
LIB2PIP = {
    "xgboost": "xgboost", "mlflow": "mlflow", "shap": "shap",
    "statsmodels": "statsmodels", "anthropic": "anthropic",
    "sentence_transformers": "sentence-transformers",
}


def detect_packages(nb):
    found = set()
    for c in nb["cells"]:
        if c["cell_type"] == "code":
            src = "".join(c["source"])
            for lib, pip in LIB2PIP.items():
                if re.search(rf"\b{re.escape(lib)}\b", src):
                    found.add(pip)
    return sorted(found)


def make_cell(cell_type, cid, source):
    cell = {"cell_type": cell_type, "id": cid, "metadata": {},
            "source": source.splitlines(keepends=True)}
    if cell_type == "code":
        cell.update(execution_count=None, outputs=[])
    return cell


def already_injected(nb):
    return any(SETUP_SENTINEL in "".join(c["source"]) for c in nb["cells"])


def inject(path, project):
    nb = json.load(open(path, encoding="utf-8"))
    if already_injected(nb):
        return "skip (موجودة)"
    pkgs = detect_packages(nb)
    md_src, code_src = cloud_setup_sources(project, pkgs)
    compile(code_src, "<setup>", "exec")           # تأكيد إن الكود سليم نحوياً
    md_cell = make_cell("markdown", "cloudsetup-md", md_src)
    code_cell = make_cell("code", "cloudsetup-code", code_src)
    insert_at = 1 if nb["cells"] else 0            # بعد عنوان النوتبوك مباشرة
    nb["cells"][insert_at:insert_at] = [md_cell, code_cell]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    return f"injected (pkgs={pkgs or '—'})"


def main():
    tracks = ["data_analysis", "ml", "data_science", "genai"]
    n = 0
    for tr in tracks:
        for proj_dir in sorted(glob.glob(os.path.join(PORTFOLIO, tr, "*", ""))):
            slug = os.path.basename(proj_dir.rstrip(os.sep))
            project = f"{tr}/{slug}"
            for nb_path in sorted(glob.glob(os.path.join(proj_dir, "*.ipynb"))):
                status = inject(nb_path, project)
                print(f"{project:42} {os.path.basename(nb_path):42} -> {status}")
                n += 1
    print(f"\nتمّت معالجة {n} نوتبوك.")


if __name__ == "__main__":
    main()
