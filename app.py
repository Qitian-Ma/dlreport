import streamlit as st
import pandas as pd
import os

# Set the title of the app
st.set_page_config(layout='wide')


password = st.text_input("请输入密码：")

if password.strip() == "onefashion":

# col1, col2 = st.columns([3, 3])

# @st.experimental_fragment
# def upload_1():
#     uploaded_file_1 = st.file_uploader("Choose a file", type=["xlsx"], key='file_1')

#     if uploaded_file_1:
#         if uploaded_file_1.type is not None:
        
#             df_1 = pd.read_excel(uploaded_file_1, engine='openpyxl', sheet_name=0)

#             st.write(df_1.head())

#             return df_1

# @st.experimental_fragment
# def upload_2():
#     uploaded_file_2 = st.file_uploader("Choose a file", type=["xlsx"], key='file2')

#     if uploaded_file_2:
#         if uploaded_file_2.type is not None:
    
#             df_2 = pd.read_excel(uploaded_file_2, engine='openpyxl', sheet_name=0)

#             st.write(df_2.head())

#             return df_2
# with col1:
#     st.title("上传在途数据")
#     zaitu_df = upload_1()
    
    
#     # Create a file uploader widget


# with col2:
#     st.title("上传入库数据")
#     storage_df = upload_2()

# @st.cache_data
# def convert_df(df):
#     # IMPORTANT: Cache the conversion to prevent computation on every rerun
#     return df.to_csv(sep=";").encode("utf-8-sig")

# # Add a button to process the uploaded file
# # merged_df = None
# st.session_state['data'] = False
# if st.button("合并", type="primary"):
#     zaitu_grouped_df = zaitu_df.groupby(["发票号码", "货号"])['数量'].sum().reset_index()
#     storage_grouped_df = storage_df.groupby(['供应商对货单号', '产品'])['数量'].sum().reset_index()
#     merged_df = zaitu_grouped_df.merge(storage_grouped_df, how="outer", left_on=['发票号码', '货号'], right_on=['供应商对货单号', '产品'], suffixes=['_在途', '_入库']).sort_values(by=['数量_在途', '数量_入库'])
#     merged_df['判断相同'] =  merged_df['数量_在途'] == merged_df['数量_入库']
#     file_out = convert_df(merged_df)
#     st.session_state['data'] = True

# if st.session_state.get('data', None) == True:
#     st.download_button(
#     label="下载为 CSV",
#     data=file_out,
#     file_name="output.csv",
#     mime="text/csv",
# )





    @st.cache_data
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv(sep=",").encode("utf-8-sig")

    @st.fragment
    def show_download():
        st.download_button(
            label="下载为 CSV",
            data=file_out,
            file_name="report.csv",
            mime="text/csv",)  
        
    st.session_state['data'] = False
    with st.form("my_form"):
        col1, col2 = st.columns([3, 3])

        with col1:
            option_shop = st.selectbox(
            "请选择门店",
            ("1BERGAMO", 
            "2FIDENZA", 
            "3HT",
            "5PARATICO",
            "6BRESCIA",
            "8CALENZANO",
            "9ROSA",
            "10THIENE",
            "11SSANVENDEMIANO",
            "12COMO",
            "13VULCANO"),
        )

        with col2:
            option_month = st.selectbox(
            "请选择月份",
            ("1", 
            "2", 
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "全部"
        ))
            
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("门店", option_shop, "月份", option_month)
            report_df = pd.read_excel(os.path.join("合并报表", option_shop + "_combined_modified_nov.xlsx"), engine='openpyxl', sheet_name=0)
            if option_month != "全部":
                report_df = report_df[report_df["日期"].dt.month == int(option_month)]
            file_out = convert_df(report_df)
            st.write(report_df)
            st.session_state['data'] = True



    if st.session_state['data']:
        show_download()
