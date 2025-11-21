import gradio as gr
import joblib
import pandas as pd


theme = gr.themes.Citrus(
    secondary_hue="yellow",
    neutral_hue="gray",
    
    text_size=gr.themes.Size(lg="16px", md="15px", sm="12px", xl="22px", xs="10px", xxl="26px", xxs="9px"),
).set(
    body_text_color='*neutral_950',
    body_text_color_dark='*neutral_50',
    body_text_color_subdued='*neutral_950',
    body_text_color_subdued_dark='*neutral_50',
    body_text_weight='500'
)

logo_html = """
<div style="text-align:center";>
<p style="font-style:italic";>Heritage Union Bank</p>
<p style="font-style:italic";>Expertise. Commitment. Value..</p>
</div>
"""
css = """
#logo-box {
    display: flex;
    justify-content: flex-start;   /* align left */
}
"""
js_func = """
function refresh() {
    const url = new URL(window.location);

    if (url.searchParams.get('__theme') !== 'dark') {
        url.searchParams.set('__theme', 'dark');
        window.location.href = url.href;
    }
}
"""

rf_model = joblib.load("loan_approval.pkl")
education_map = {"Graduate":0,"Not Graduate":1}
employed_map = {"No":0,"Yes":1}
def predict_loan(no_dependents,edu,self_employed,income_anum,loan_amt,loan_term,credit_score,rav, cav,lav,bav):
    try:
        edcation_enc = education_map[edu]
        employed_enc = employed_map[self_employed]
        input_data = pd.DataFrame({"no_of_dependents":[no_dependents],
        "education":[edcation_enc],
        "self_employed":[employed_enc],
        "income_annum":[income_anum],
        "loan_amount":[loan_amt],
        "loan_term":[loan_term],
        "credit_score":[credit_score],
        "residential_assets_value":[rav],
        "commercial_assets_value":[cav],
        "luxury_assets_value":[lav],
        "bank_asset_value":[bav]    
        })
        if all([no_dependents,edu,self_employed,income_anum,loan_amt,loan_term,credit_score,rav, cav,lav,bav]):
            prediction= rf_model.predict(input_data)[0]
        else:
            return "Form must be filled completely"
    except KeyError:
       return "Please fill form!"
   
    if prediction == 0:
        feedback="Congratulations!! your loan will be approved.\nYour account will be creditted in less than 24hours.Thank you"
        
    else:
        feedback="Unfortunately we will not be able to approve your loan at this time.\nVisit our branches to speak to a consultant.Thank you."
    
    return feedback


form = gr.Interface(fn=predict_loan,inputs=[gr.Number(label="Number of Dependents"),
                        gr.Dropdown(["Graduate", "Not Graduate"], label="Education",value=None),
                        gr.Dropdown(["Yes", "No"],label="Self Employed?", value=None),
                        gr.Number(label="Income Per Annum (₦)"),
                        gr.Number(label="Loan Amount (₦)"),
                        gr.Slider(minimum=0,maximum=20, label="Loan Term",step=1),
                        gr.Slider(minimum=300, maximum=950, label="Credit Score"),
                        gr.Number(label="Resedential Assets Value (₦)"), 
                        gr.Number(label="Commercial Assets Value (₦)"),
                        gr.Number(label="Luxury Assets Value (₦)"), 
                        gr.Number(label="Bank Assets Value (₦)"),
                        
                                        
                                            ],outputs=gr.Textbox(lines=3, label="Message To Applicant"),title="Loan Application Form", flagging_mode="never"
                                            
                                            )

with gr.Blocks(theme=theme, css=css,title="Loan Application Form", js=js_func) as demo:
     with gr.Row():
        with gr.Column():
            gr.Image("HUBLogo.gif",
                elem_id="logo-box",
                show_label=False, height=120, show_download_button=False, show_fullscreen_button=False, container=False
            )

     form.render()
     gr.HTML(logo_html)
demo.launch(auth=("Customer","group4"))
