"""
Install the Google AI Python SDK

$ pip install google-generativeai
"""

import os
import google.generativeai as genai

genai.configure(api_key="AIzaSyAQqC3zoOsvabTZ7R7poU1jUzUHwJc6aNg")

# Create the model
generation_config = {
  "temperature": 0.2,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="consice and precise, also explain in layman's terms.Generate a detailed and patient-friendly discharge report that includes explanations for the patient's disease, the reasoning behind the patient's condition based on their current information and past medical history, as well as the rationale for the prescribed medications or treatments. The report should also provide post-discharge instructions, including AI recommendations for temporary lifestyle changes and future prevention measures. Additional information such as past medical history and lab test results should be considered, and if any information is missing, it should be indicated as 'None' or 'Nil.' If only one date is provided, the date of discharge is not required in the report. Do not explain the physical symptoms, but instead, focus on why the recommended medications only were prescribed for the patient and why not similar ones, taking into account their current condition and symptoms, as well as any relevant historical data. Additionally, provide an explanation for why alternative medications serving a similar purpose were not recommended, if applicable. Include the doctor's name and ID in the report.",
)

chat_session = model.start_chat(
  history=[
  ]
)

response = chat_session.send_message("Patient information: 05-09-2024,patient id:69,vidhun, 21, aids, 3 days, symptoms: {cold, tiredness},past history: no severe issues, doctor: Dr.Gopi, doctor id:6989,medications: paracetamol, follow ups: none.")

print(response.text)