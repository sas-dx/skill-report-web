#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SQLサンプルデータから Prisma 用 seed.ts を生成するスクリプト

スクリプトの目的
---------------
docs/design/database/data 配下にある `*_sample_data.sql` ファイルを読み取り、
Prisma Client で利用できる `seed.ts` コードを生成します。

使い方
------
python3 scripts/sql-to-seed-prisma-fixed.py <sql_dir> [output_file]

- output_file を省略すると `"src/database/prisma/seed.ts"` に出力します。
- テーブル名・カラム名は **そのまま snake_case** で出力します。
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple, Any


# --------------------------------------------------------------------------- #
# 名称変換ユーティリティ
# --------------------------------------------------------------------------- #
def to_model_name(name: str) -> str:
    """テーブル名 'MST_Tenant' → モデル名 'Tenant'"""
    name = re.sub(r"^([A-Z]+_)", "", name)
    return re.sub(r"(?:^|_)([A-Za-z])", lambda m: m.group(1).upper(), name)


def to_prisma_property(name: str) -> str:
    """Prisma クライアントのプロパティ名 (camelCase) を返す"""
    model = to_model_name(name)
    return model[:1].lower() + model[1:]


# --------------------------------------------------------------------------- #
# SQL 解析
# --------------------------------------------------------------------------- #
def parse_sql_file(path: Path) -> Tuple[str, List[str], List[List[Any]]]:
    """
    INSERT 文を含む SQL ファイルを解析し、
    (テーブル名, カラム一覧, 行データ) を返す。
    """
    content = path.read_text(encoding="utf-8")

    match = re.search(
        r"INSERT\s+INTO\s+(\w+)\s*\(([^)]*)\)\s*VALUES\s*(.*?);\s*$",
        content,
        re.S,
    )
    if not match:
        raise ValueError(f"INSERT 文が見つかりません: {path}")

    table = match.group(1)
    columns = [c.strip() for c in match.group(2).split(",")]

    values_block = match.group(3)

    # ――― VALUES 句を ( … ),( … ) … に分割（クォート内のカッコを無視） ――― #
    row_texts: List[str] = []
    buf: List[str] = []
    in_quote = False
    escape = False
    depth = 0

    for ch in values_block:
        if ch == "'" and not escape:
            in_quote = not in_quote
        if ch == "\\" and in_quote:
            escape = not escape
            buf.append(ch)
            continue
        else:
            escape = False

        if ch == "(" and not in_quote:
            if depth == 0:
                buf = []
            else:
                buf.append(ch)
            depth += 1
            continue
        if ch == ")" and not in_quote:
            depth -= 1
            if depth == 0:
                row_texts.append("".join(buf).strip())
                continue
            else:
                buf.append(ch)
                continue

        if depth > 0:
            buf.append(ch)

    # ――― 行データをパース ――― #
    rows: List[List[Any]] = []
    for row_text in row_texts:
        fields: List[Any] = []
        # カンマ分割（クォート内は無視）
        for val in re.split(r",(?=(?:[^']*'[^']*')*[^']*$)", row_text):
            val = val.strip()
            if val.upper() == "NULL":
                fields.append(None)
            elif val.upper() == "TRUE":
                fields.append(True)
            elif val.upper() == "FALSE":
                fields.append(False)
            else:
                if val.startswith("'") and val.endswith("'"):
                    fields.append(val[1:-1].replace("\\'", "'"))
                else:
                    fields.append(val)
        rows.append(fields)

    return table, columns, rows


# --------------------------------------------------------------------------- #
# TypeScript 生成
# --------------------------------------------------------------------------- #
def format_value(value: Any) -> str:
    """Python の値を TypeScript リテラルへ変換"""
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, str) and re.match(r"^-?\d+(\.\d+)?$", value):
        # 数値のまま文字列に入っていたケースを数値扱い
        return value
    if isinstance(value, str):
        return f'"{value}"'
    return str(value)


def generate_ts(table: str, columns: List[str], rows: List[List[Any]]) -> str:
    """Prisma 用の TypeScript コード片を生成"""
    lines: List[str] = []
    model_prop = to_prisma_property(table)

    lines.append(f"console.log('📊 {table} データを投入中…')")
    lines.append(f"await prisma.{model_prop}.createMany({{")
    lines.append("  data: [")
    for row in rows:
        lines.append("    {")
        for col, val in zip(columns, row):
            lines.append(f"      {col}: {format_value(val)},")
        lines.append("    },")
    lines.append("  ],")
    lines.append("})")

    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# メイン
# --------------------------------------------------------------------------- #
def main(sql_dir: str, output_file: str) -> None:
    sql_path = Path(sql_dir)
    out_path = Path(output_file)

    snippets: List[str] = []
    for sql_file in sorted(sql_path.glob("*_sample_data.sql")):
        table, columns, rows = parse_sql_file(sql_file)
        snippets.append(f"// {sql_file.name}\n{generate_ts(table, columns, rows)}\n")

    header = [
        "// Auto generated by sql-to-seed-prisma-fixed.py",
        "import { PrismaClient } from '@prisma/client'",
        "",
        "const prisma = new PrismaClient()",
        "",
        "export async function runSampleSeed() {",
        "  console.log('🌱 データベースの初期データ投入を開始します…')",
    ]
    footer = [
        "  console.log('✅ 初期データ投入が完了しました！')",
        "}",
        "",
        "if (require.main === module) {",
        "  runSampleSeed().then(() => prisma.$disconnect())",
        "}",
    ]

    # 出力先ディレクトリを作成
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(header) + "\n")
        for snippet in snippets:
            # 関数内インデントをそろえる
            f.write("  " + snippet.replace("\n", "\n  ") + "\n")
        f.write("\n".join(footer) + "\n")


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print("Usage: python sql-to-seed-prisma-fixed.py <sql_dir> [output_file]")
        sys.exit(1)

    sql_dir = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) == 3 else "src/database/prisma/seed.ts"
    main(sql_dir, out_file)
