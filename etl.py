# pip install pandas openpyxl unidecode python-dateutil
import re
import pandas as pd
from unidecode import unidecode
from dateutil import parser

# -------- utilidades --------
def padroniza_nome(col: str) -> str:
    col = unidecode(str(col)).strip().lower()
    col = re.sub(r"[\s/|-]+", "_", col)
    col = re.sub(r"[^a-z0-9_]", "", col)
    return col

SINONIMOS = {
    # identificadores
    "id_cliente": ["id", "idcliente", "cod_cliente", "codigo_cliente"],
    "cpf_cnpj": ["cpf", "cpfcnpj", "documento", "doc", "cnpj"],
    "nome": ["cliente", "nome_cliente", "razao_social", "nome_completo"],
    # contatos
    "email": ["e_mail", "correio", "email_principal"],
    "telefone": ["tel", "celular", "fone", "telefone1", "telefone_principal"],
    "cidade": ["municipio", "cidade_uf", "localidade"],
    "estado": ["uf", "estado_uf"],
    # negócio
    "consultor": ["assessor", "responsavel", "consultor_responsavel"],
    "segmento": ["perfil", "ocupacao", "categoria", "nicho"],
    "status": ["estagio", "pipeline_status", "situacao"],
    "pl": ["patrimonio", "aum", "saldo", "pl_total", "patrimonio_financeiro"],
    "ticket_medio": ["ticket", "ticketmedio"],
    "data_inicio": ["data_onboarding", "inicio_relacao", "data_entrada"],
    "aniversario": ["data_nascimento", "nascimento", "birthday"],
}

def aplica_sinonimos(cols):
    mapeamento = {}
    pad_cols = [padroniza_nome(c) for c in cols]
    for destino, aliases in SINONIMOS.items():
        alvos = set([destino] + [padroniza_nome(a) for a in aliases])
        for c in pad_cols:
            if c in alvos:
                mapeamento[c] = destino
    return mapeamento

def to_decimal_brasil(x):
    if pd.isna(x):
        return pd.NA
    s = str(x).strip()
    if s == "" or s.lower() in {"nan", "none", "nd"}:
        return pd.NA
    # remove separador de milhar . e troca vírgula por ponto
    s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except Exception:
        # às vezes já vem como número
        try:
            return float(x)
        except Exception:
            return pd.NA

def to_date_br(x):
    if pd.isna(x) or str(x).strip() == "":
        return pd.NaT
    try:
        # dayfirst=True para dd/mm/aaaa
        return parser.parse(str(x), dayfirst=True, fuzzy=True)
    except Exception:
        return pd.NaT

def padroniza_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # renomeia colunas cruas
    original_cols = list(df.columns)
    cols_pad = [padroniza_nome(c) for c in original_cols]
    df.columns = cols_pad

    # aplica dicionário de sinônimos
    ren = aplica_sinonimos(df.columns)
    df = df.rename(columns=ren)

    # tipos: monetários e datas (heurística por nome)
    for c in df.columns:
        if re.search(r"(pl|patrimonio|saldo|aum|renda|ticket)", c):
            df[c] = df[c].apply(to_decimal_brasil)
        if re.search(r"(data|aniversario|nascimento|inicio)", c):
            df[c] = df[c].apply(to_date_br)

    # strip strings
    for c in df.select_dtypes(include=["object"]).columns:
        df[c] = df[c].astype(str).str.strip().replace({"nan": pd.NA, "None": pd.NA})

    # cria chaves auxiliares se ausentes
    if "id_cliente" not in df.columns and "cpf_cnpj" not in df.columns:
        # tenta construir uma chave a partir do nome+email (fallback)
        if {"nome", "email"} <= set(df.columns):
            df["id_fallback"] = (
                df["nome"].fillna("").str.lower().str.strip()
                + "||"
                + df["email"].fillna("").str.lower().str.strip()
            )
        else:
            df["id_fallback"] = df.index.astype(str)
    return df

# -------- leitura e merge --------
def carrega_base(caminho: str, sheet_name=0) -> pd.DataFrame:
    df = pd.read_excel(caminho, sheet_name=sheet_name, engine="openpyxl")
    return padroniza_dataframe(df)

def merge_bases(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    # define melhor chave disponível
    if "id_cliente" in df1.columns and "id_cliente" in df2.columns:
        chave = "id_cliente"
    elif "cpf_cnpj" in df1.columns and "cpf_cnpj" in df2.columns:
        chave = "cpf_cnpj"
    else:
        chave = "id_fallback"

    # garante existência da chave fallback
    for d in (df1, df2):
        if chave not in d.columns:
            if "id_fallback" not in d.columns:
                base = d.copy()
                id_cols = [c for c in ["nome", "email"] if c in base.columns]
                if id_cols:
                    base["id_fallback"] = (
                        base[id_cols].astype(str).agg("||".join, axis=1).str.lower()
                    )
                else:
                    base["id_fallback"] = base.index.astype(str)
                d["id_fallback"] = base["id_fallback"]

    df = pd.merge(df1, df2, on=chave, how="outer", suffixes=("_a", "_b"))
    # remove colunas 100% vazias
    df = df.dropna(axis=1, how="all")
    return df, chave

if __name__ == "__main__":
    arq1 = "BASE DE CLIENTES CONSULTOR BELFORT.xlsx"
    arq2 = "BASE-CADASTRAL-CLIENTES.xlsx"

    base1 = carrega_base(arq1)
    base2 = carrega_base(arq2)

    unificada, chave = merge_bases(base1, base2)

    # Relatório rápido de qualidade
    print(f"Chave de merge utilizada: {chave}")
    print("\nColunas padronizadas:")
    print(sorted(unificada.columns))

    print("\nAmostra (5 linhas):")
    print(unificada.head(5))

    print("\nNulos por coluna (%):")
    print((unificada.isna().mean() * 100).round(1).sort_values(ascending=False))
