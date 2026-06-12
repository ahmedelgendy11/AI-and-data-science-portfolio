# -*- coding: utf-8 -*-
"""Shared helper to build paired (exercise + solution) notebooks from one cell list."""
import json, os

# مصدر واحد لرابط الريبو — غيّره هنا لو اتغيّر اسم/حساب الريبو، وأعد توليد/حقن النوتبوكات.
REPO_URL = "https://github.com/Ahmedelgendyyy/data-science-portfolio"
SETUP_SENTINEL = "إعداد تلقائي — Colab"   # علامة لمنع تكرار حقن خلية الإعداد


def cloud_setup_sources(project, packages=()):
    """يرجّع (markdown, code) لخلية إعداد تشتغل على Colab/Kaggle/محلي (no-op محلياً)."""
    md = ("## 🚀 إعداد التشغيل (Colab · Kaggle · محلي)\n"
          "الخلية الجاية بتثبّت المكتبات الناقصة وتجيب الداتا تلقائياً على Colab/Kaggle.\n"
          "**محلياً** (بالـ env بتاع المشروع) هي مجرد no-op — تقدر تتجاهلها.")
    pkgs = ", ".join('"%s"' % p for p in packages)
    code = (
        "# 🚀 إعداد تلقائي — Colab / Kaggle / محلي (no-op محلياً)\n"
        "import os, sys, subprocess, importlib.util\n"
        'REPO    = "%s"\n'
        'PROJECT = "%s"          # مسار المشروع داخل portfolio/\n'
        "PKGS    = [%s]          # مكتبات المشروع (تتثبّت لو ناقصة)\n"
        "for _pkg in PKGS:\n"
        '    if importlib.util.find_spec(_pkg.replace("-", "_")) is None:\n'
        '        subprocess.run([sys.executable, "-m", "pip", "install", "-q", _pkg])\n'
        'if not os.path.isdir("data"):                 # سحابياً: نجيب الريبو ونروح لمجلد المشروع\n'
        '    _clone = REPO.rstrip("/").split("/")[-1]\n'
        '    if not os.path.isdir(_clone):\n'
        '        subprocess.run(["git", "clone", "-q", REPO + ".git"])\n'
        '    os.chdir(os.path.join(_clone, "portfolio", PROJECT))\n'
        'print("✓ جاهز —", os.getcwd())'
    ) % (REPO_URL, project, pkgs)
    return md, code


class NB:
    def __init__(self):
        self.cells = []

    def md(self, text):
        self.cells.append(("md", text))

    def code(self, solution_src, stub=None):
        self.cells.append(("code", solution_src, stub))

    def cloud_setup(self, project, packages=()):
        """يضيف خلية إعداد تشغّل المشروع على Colab/Kaggle/محلي. project مثل 'ml/b1_churn_prediction'."""
        md_src, code_src = cloud_setup_sources(project, packages)
        self.cells.append(("md", md_src))
        self.cells.append(("code", code_src, code_src))

    def _to_nb(self, solution=True):
        out = []
        for idx, c in enumerate(self.cells):
            cid = f"cell{idx:02d}"
            if c[0] == "md":
                out.append({"cell_type": "markdown", "id": cid, "metadata": {},
                            "source": c[1].splitlines(keepends=True)})
            else:
                src = c[1] if (solution or c[2] is None) else c[2]
                out.append({"cell_type": "code", "id": cid, "metadata": {},
                            "execution_count": None, "outputs": [],
                            "source": src.splitlines(keepends=True)})
        return {"cells": out,
                "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python",
                                            "name": "python3"},
                             "language_info": {"name": "python"}},
                "nbformat": 4, "nbformat_minor": 5}

    def write(self, base_dir, slug):
        paths = []
        for sol, name in [(True, "solution"), (False, "exercise")]:
            p = os.path.join(base_dir, f"{slug}_{name}.ipynb")
            with open(p, "w", encoding="utf-8") as f:
                json.dump(self._to_nb(sol), f, ensure_ascii=False, indent=1)
            paths.append(p)
        print("wrote:", *[os.path.basename(p) for p in paths])
        return paths
