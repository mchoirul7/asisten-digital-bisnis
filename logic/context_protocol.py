import google.generativeai as genai
import pandas as pd

class ContextProtocol:
    def __init__(self, api_key: str, model_name="gemini-1.5-flash-latest"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def ask(self, prompt: str, context) -> str:
        if isinstance(context, pd.DataFrame):
            context_str = context.to_markdown(index=False)
            note = "Berikut adalah tabel ringkasan performa produk:"
        elif isinstance(context, str):
            context_str = context
            note = "Berikut adalah data ringkasan dari sistem:"
        else:
            raise ValueError("Context harus berupa DataFrame atau string.")

        full_prompt = f"""{note}

    {context_str}

    Silakan analisis dan berikan insight bisnis secara naratif:
    - Sebutkan produk yang cepat laku, lambat, dan tidak laku
    - Berikan saran: restock, diskon, bundling, atau penghentian
    - Gunakan gaya bahasa formal dan profesional yang sesuai untuk laporan bisnis
    - Gunakan format markdown untuk penekanan seperti judul, bullet, dan angka

    {prompt}

    Jawaban:
    """
        response = self.model.generate_content(full_prompt, generation_config={"temperature": 0.2})

        return response.text.strip() if response.text else "Tidak ada jawaban."

