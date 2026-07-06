import streamlit as st
import pickle
import numpy as np

st.set_page_config(page_title="💧 Water Potability Predictor", layout="wide")

st.markdown("""
<style>
.stApp {background: linear-gradient(135deg,#0f172a,#1e3a8a);}
h1,h3,label,p{color:white!important;}
div[data-testid="stMetric"]{background:#ffffff22;padding:10px;border-radius:12px;}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    with open("model.pkl","rb") as f:
        return pickle.load(f)

try:
    model=load_model()
except Exception:
    st.error("model.pkl not found. Place the trained model beside app.py")
    st.stop()

st.title("💧 Water Potability Prediction")
st.write("Enter water quality parameters and click **Predict**.")

cols=st.columns(3)
names=[
("pH",7.0),("Hardness",200.0),("Solids",20000.0),
("Chloramines",7.0),("Sulfate",330.0),("Conductivity",420.0),
("Organic_carbon",14.0),("Trihalomethanes",66.0),("Turbidity",4.0)
]
vals=[]
for i,(n,d) in enumerate(names):
    with cols[i%3]:
        vals.append(st.number_input(n,value=float(d)))

if st.button("🔍 Predict", use_container_width=True):
    arr=np.array([vals])
    pred=model.predict(arr)[0]
    try:
        prob=model.predict_proba(arr)[0][1]
    except Exception:
        prob=None
    if pred==1:
        st.success("✅ Water is POTABLE (Safe to drink)")
    else:
        st.error("❌ Water is NOT POTABLE")
    if prob is not None:
        st.metric("Confidence (Potable)", f"{prob*100:.2f}%")
