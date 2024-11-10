import os
from dotenv import load_dotenv
load_dotenv()

import json
import openai
import utils

json_file_current_form = " data/current.json"
model = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"

def set_i765_1st_page(reason=None, legal_names=None, is_g28_attached=None, uscis_online_account_number=None):
    current_form = utils.read_json_current_form(json_file_current_form=json_file_current_form)
    
    if reason:
        current_form["form1[0].Page1[0].Part1_Checkbox[0]"] = "Off"
        current_form["form1[0].Page1[0].Part1_Checkbox[1]"] = "Off"
        current_form["form1[0].Page1[0].Part1_Checkbox[2]"] = "Off"

        if reason == "initial":
            current_form["form1[0].Page1[0].Part1_Checkbox[0]"] = "1"
        elif reason == "replace":
            current_form["form1[0].Page1[0].Part1_Checkbox[1]"] = "2"
        elif reason == "renewal":
            current_form["form1[0].Page1[0].Part1_Checkbox[2]"] = "3"
        else:
            pass

    if legal_names:
        for i, full_name in legal_names.items():
            full_name = full_name.split(" ")
            if i == '1':
                current_form["form1[0].Page1[0].Line1a_FamilyName[0]"] = full_name[-1]
                current_form["form1[0].Page1[0].Line1b_GivenName[0]"] = full_name[0]
                current_form["form1[0].Page1[0].Line1c_MiddleName[0]"] = full_name[1] if len(full_name) == 3 else ""
            if i == '2':
                current_form["form1[0].Page1[0].Line2a_FamilyName[0]"] = full_name[-1]
                current_form["form1[0].Page1[0].Line2b_GivenName[0]"] = full_name[0]
                current_form["form1[0].Page1[0].Line2c_MiddleName[0]"] = full_name[1] if len(full_name) == 3 else ""
            if i == '3':
                current_form["form1[0].Page1[0].Line3a_FamilyName[1]"] = full_name[-1]
                current_form["form1[0].Page1[0].Line3b_GivenName[1]"] = full_name[0]
                current_form["form1[0].Page1[0].Line3c_MiddleName[1]"] = full_name[1] if len(full_name) == 3 else ""
            if i == '4':
                current_form["form1[0].Page1[0].Line3a_FamilyName[0]"] = full_name[-1]
                current_form["form1[0].Page1[0].Line3b_GivenName[0]"] = full_name[0]
                current_form["form1[0].Page1[0].Line3c_MiddleName[0]"] = full_name[1] if len(full_name) == 3 else ""

    if is_g28_attached:
        if is_g28_attached == "yes":
            current_form["form1[0].Page1[0].CheckBox1[0]"] = "1"
        else:
            current_form["form1[0].Page1[0].CheckBox1[0]"] = "Off"

    if uscis_online_account_number:
        current_form["form1[0].Page1[0].USCISELISAcctNumber[0]"] = uscis_online_account_number

    utils.write_json_and_pdf_form(current_form, json_file_current_form)

    return "Complete"

def set_i765_2nd_page_us_mail_addr(in_care_of_name=None, street=None, res_cat=None, city_town=None, state=None, zip_code=None, is_same_physical=None):
    current_form = utils.read_json_current_form(json_file_current_form=json_file_current_form)

    if in_care_of_name:
        current_form["form1[0].Page2[0].Line4a_InCareofName[0]"] = in_care_of_name

    if street:
        current_form["form1[0].Page2[0].Line4b_StreetNumberName[0]"] = street

    if res_cat:
        current_form["form1[0].Page2[0].Pt2Line5_Unit[0]"] = "Off"
        current_form["form1[0].Page2[0].Pt2Line5_Unit[1]"] = "Off"
        current_form["form1[0].Page2[0].Pt2Line5_Unit[2]"] = "Off"

        if res_cat["cat"] == "ste":
            current_form["form1[0].Page2[0].Pt2Line5_Unit[0]"] = " STE "
        elif res_cat["cat"] == "flr":
            current_form["form1[0].Page2[0].Pt2Line5_Unit[1]"] = " FLR "
        elif res_cat["cat"] == "apt":
            current_form["form1[0].Page2[0].Pt2Line5_Unit[2]"] = " APT "
        else:
            pass

        current_form["form1[0].Page2[0].Pt2Line5_AptSteFlrNumber[0]"] = res_cat["name"]

    if city_town:
        current_form["form1[0].Page2[0].Pt2Line5_CityOrTown[0]"] = city_town

    if state:
        current_form["form1[0].Page2[0].Pt2Line5_State[0]"] = state

    if zip_code:
        current_form["form1[0].Page2[0].Pt2Line5_ZipCode[0]"] = zip_code        

    if is_same_physical: # Off
        current_form["form1[0].Page2[0].Part2Line5_Checkbox[0]"] = "Off"
        current_form["form1[0].Page2[0].Part2Line5_Checkbox[1]"] = "Off"

        if is_same_physical == "yes":
            current_form["form1[0].Page2[0].Part2Line5_Checkbox[1]"] = "Y"
        else:
            current_form["form1[0].Page2[0].Part2Line5_Checkbox[0]"] = "N"

    utils.write_json_and_pdf_form(current_form, json_file_current_form)

    return "Complete"

def set_i765_2nd_page_us_physic_addr(street=None, res_cat=None, city_town=None, state=None, zip_code=None):
    current_form = utils.read_json_current_form(json_file_current_form=json_file_current_form)

    if street:
        current_form["form1[0].Page2[0].Pt2Line7_StreetNumberName[0]"] = street

    if res_cat:
        current_form["form1[0].Page2[0].Pt2Line7_Unit[0]"] = "Off"
        current_form["form1[0].Page2[0].Pt2Line7_Unit[1]"] = "Off"
        current_form["form1[0].Page2[0].Pt2Line7_Unit[2]"] = "Off"

        if res_cat["cat"] == "ste":
            current_form["form1[0].Page2[0].Pt2Line7_Unit[0]"] = " STE "
        elif res_cat["cat"] == "flr":
            current_form["form1[0].Page2[0].Pt2Line7_Unit[1]"] = " FLR "
        elif res_cat["cat"] == "apt":
            current_form["form1[0].Page2[0].Pt2Line7_Unit[2]"] = " APT "
        else:
            pass

        current_form["form1[0].Page2[0].Pt2Line7_AptSteFlrNumber[0]"] = res_cat["name"]

    if city_town:
        current_form["form1[0].Page2[0].Pt2Line7_CityOrTown[0]"] = city_town

    if state:
        current_form["form1[0].Page2[0].Pt2Line7_State[0]"] = state

    if zip_code:
        current_form["form1[0].Page2[0].Pt2Line7_ZipCode[0]"] = zip_code

    utils.write_json_and_pdf_form(current_form, json_file_current_form)

    return "Complete"

def set_i765_2nd_page_personal_info(a_number=None, uscis_online_account_number=None, gender=None, marital_status=None, filed_i765_before=None, ssc=None, issue_ssc=None, father_name=None, mother_name=None, citizenship=None):
    current_form = utils.read_json_current_form(json_file_current_form=json_file_current_form)

    if a_number:
        current_form["form1[0].Page2[0].Line7_AlienNumber[0]"] = a_number

    if uscis_online_account_number:
        current_form["form1[0].Page2[0].Line8_ElisAccountNumber[0]"] = uscis_online_account_number

    if gender:
        current_form["form1[0].Page2[0].Line9_Checkbox[0]"] = "Off"
        current_form["form1[0].Page2[0].Line9_Checkbox[1]"] = "Off"

        if gender == "male":
            current_form["form1[0].Page2[0].Line9_Checkbox[1]"] = "Y"
        else:
            current_form["form1[0].Page2[0].Line9_Checkbox[0]"] = "N"

    if marital_status:
        current_form["form1[0].Page2[0].Line10_Checkbox[0]"] = "Off"
        current_form["form1[0].Page2[0].Line10_Checkbox[1]"] = "Off"
        current_form["form1[0].Page2[0].Line10_Checkbox[2]"] = "Off"
        current_form["form1[0].Page2[0].Line10_Checkbox[3]"] = "Off"

        if marital_status == "single":
            current_form["form1[0].Page2[0].Line10_Checkbox[2]"] = "Single"
        elif marital_status == "married":
            current_form["form1[0].Page2[0].Line10_Checkbox[3]"] = "Married"
        elif marital_status == "divorced":
            current_form["form1[0].Page2[0].Line10_Checkbox[1]"] = "Divorced"
        else:
            current_form["form1[0].Page2[0].Line10_Checkbox[1]"] = "Widowed"

    if filed_i765_before:
        current_form["form1[0].Page2[0].Line13_Checkbox[0]"] = "Off"
        current_form["form1[0].Page2[0].Line13_Checkbox[1]"] = "Off"

        if filed_i765_before == "yes":
            current_form["form1[0].Page2[0].Line13_Checkbox[1]"] = "Y"
        else:
            current_form["form1[0].Page2[0].Line13_Checkbox[0]"] = "N"

    if ssc:
        current_form["form1[0].Page2[0].Line12a_Checkbox[0]"] = "Off"
        current_form["form1[0].Page2[0].Line12a_Checkbox[1]"] = "Off"
        current_form["form1[0].Page2[0].Line12b_SSN[0]"] = ""

        if ssc["card"] == "yes":
            current_form["form1[0].Page2[0].Line12a_Checkbox[1]"] = "Y"
            current_form["form1[0].Page2[0].Line12b_SSN[0]"] = ssc.get("ssn", "")
        else:
            current_form["form1[0].Page2[0].Line12a_Checkbox[0]"] = "N"

    if father_name:
        full_name = issue_ssc.get("father", "").split(" ")
        current_form["form1[0].Page2[0].Line15a_FamilyName[0]"] = full_name[-1]
        current_form["form1[0].Page2[0].Line15b_GivenName[0]"] = full_name[0]

    if mother_name:
        full_name = issue_ssc.get("mother", "").split(" ")
        current_form["form1[0].Page2[0].Line16a_FamilyName[0]"] = full_name[-1]
        current_form["form1[0].Page2[0].Line16b_GivenName[0]"] = full_name[0]

    if issue_ssc:
        current_form["form1[0].Page2[0].Line19_Checkbox[0]"] = "Off"
        current_form["form1[0].Page2[0].Line19_Checkbox[1]"] = "Off"
        current_form["form1[0].Page2[0].Line14_Checkbox_No[0]"] = "Off"
        current_form["form1[0].Page2[0].Line14_Checkbox_Yes[0]"] = "Off"
        
        current_form["form1[0].Page2[0].Line16a_FamilyName[0]"] = ""
        current_form["form1[0].Page2[0].Line16b_GivenName[0]"] = ""

        if issue_ssc["issue"] == "no":
            current_form["form1[0].Page2[0].Line19_Checkbox[0]"] = "N"
        else:
            current_form["form1[0].Page2[0].Line19_Checkbox[1]"] = "Y"
            if issue_ssc.get("disc") == "no":
                current_form["form1[0].Page2[0].Line14_Checkbox_No[0]"] = "1"
            else:
                current_form["form1[0].Page2[0].Line14_Checkbox_Yes[0]"] = "1"

    if citizenship:
        current_form["form1[0].Page2[0].Line17a_CountryOfBirth[0]"] = ""
        current_form["form1[0].Page2[0].Line17b_CountryOfBirth[0]"] = ""

        if len(citizenship) == 0:
            pass
        elif len(citizenship) == 1:
            current_form["form1[0].Page2[0].Line17a_CountryOfBirth[0]"] = citizenship[0]
        else:
            current_form["form1[0].Page2[0].Line17a_CountryOfBirth[0]"] = citizenship[0]
            current_form["form1[0].Page2[0].Line17b_CountryOfBirth[0]"] = citizenship[1]

    utils.write_json_and_pdf_form(current_form, json_file_current_form)

    return "Complete"

def set_i765_3rd_page_place_birth(city=None, state=None, country=None, dob=None):
    current_form = utils.read_json_current_form(json_file_current_form=json_file_current_form)

    if city:
        current_form["form1[0].Page3[0].Line18a_CityTownOfBirth[0]"] = city

    if state:
        current_form["form1[0].Page3[0].Line18b_CityTownOfBirth[0]"] = state

    if country:
        current_form["form1[0].Page3[0].Line18c_CountryOfBirth[0]"] = country

    if dob:
        current_form["form1[0].Page3[0].Line19_DOB[0]"] = dob

    utils.write_json_and_pdf_form(current_form, json_file_current_form)

    return "Complete"

def set_i765_3rd_page_last_us_arrival(arr_dep_num=None, pass_num=None, trav_doc_num=None, country_issue=None, exp_date=None, last_date_us=None, last_place_us=None, immg_status_last_arr=None, cur_immg_status=None, sevis=None):
    current_form = utils.read_json_current_form(json_file_current_form=json_file_current_form)

    if arr_dep_num:
        current_form["form1[0].Page3[0].Line20a_I94Number[0]"] = arr_dep_num

    if pass_num:
        current_form["form1[0].Page3[0].Line20b_Passport[0]"] = pass_num

    if trav_doc_num:
        current_form["form1[0].Page3[0].Line20c_TravelDoc[0]"] = trav_doc_num

    if country_issue:
        current_form["form1[0].Page3[0].Line20d_CountryOfIssuance[0]"] = country_issue
    
    if exp_date:
        current_form["form1[0].Page3[0].Line20e_ExpDate[0]"] = exp_date

    if last_date_us:
        current_form["form1[0].Page3[0].Line21_DateOfLastEntry[0]"] = last_date_us

    if last_place_us:
        current_form["form1[0].Page3[0].place_entry[0]"] = last_place_us

    if immg_status_last_arr:
        current_form["form1[0].Page3[0].Line23_StatusLastEntry[0]"] = immg_status_last_arr

    if cur_immg_status:
        current_form["form1[0].Page3[0].Line24_CurrentStatus[0]"] = cur_immg_status

    if sevis:
        current_form["form1[0].Page3[0].Line26_SEVISnumber[0]"] = sevis

    utils.write_json_and_pdf_form(current_form, json_file_current_form)

    return "Complete"

def set_i765_3rd_page_elig_cat(elig_cat=None, c3c_stem=None, c26=None, c8=None, c35_c36=None):
    current_form = utils.read_json_current_form(json_file_current_form=json_file_current_form)

    if elig_cat:
        elig_cat = elig_cat.lstrip("(").rstrip(")").split(")(")
        current_form["form1[0].Page3[0].#area[1].section_1[0]"] = elig_cat[0] if len(elig_cat) > 0 else ""
        current_form["form1[0].Page3[0].#area[1].section_2[0]"] = elig_cat[1] if len(elig_cat) > 1 else ""
        current_form["form1[0].Page3[0].#area[1].section_3[0]"] = elig_cat[2] if len(elig_cat) > 2 else ""

    if c3c_stem:
        current_form["form1[0].Page3[0].Line27a_Degree[0]"] = c3c_stem.get("degree", "")
        current_form["form1[0].Page3[0].Line27b_Everify[0]"] = c3c_stem.get("emp_name", "")
        current_form["form1[0].Page3[0].Line27c_EverifyIDNumber[0]"] = c3c_stem.get("e_verify", "")
        
    if c26:
        current_form["form1[0].Page3[0].Line28_ReceiptNumber[0]"] = c26
                   
    if c8:
        current_form["form1[0].Page3[0].PtLine29_YesNo[0]"] = "Y" if c8=="yes" else "Off"
        current_form["form1[0].Page3[0].Line28_ReceiptNumber[0]"] = "N" if c8=="no" else "Off"     

    if c35_c36:
        current_form["form1[0].Page3[0].Line18a_Receipt[0].Line30a_ReceiptNumber[0]"] = c35_c36.get("rec_num", "")
        current_form["form1[0].Page3[0].Line18a_Receipt[0].PtLine30b_YesNo[0]"] = "Y" if c35_c36.get("crime") == "yes" else "Off"
        current_form["form1[0].Page3[0].Line18a_Receipt[0].PtLine30b_YesNo[1]"] = "N" if c35_c36.get("crime") == "no" else "Off"

    utils.write_json_and_pdf_form(current_form, json_file_current_form)

    return "Complete"

def set_i765_4th_page_applicant(use_interpreter=None, use_preparer=None, daytime_tel=None, mobile_tel=None, email_addr=None, is_salva_guate=None, sign_date=None):
    current_form = utils.read_json_current_form(json_file_current_form=json_file_current_form)

    if use_interpreter:
        current_form["form1[0].Page4[0].Pt3Line1Checkbox[0]"] = "B" if use_interpreter == "yes" else "Off"
        current_form["form1[0].Page4[0].Pt3Line1Checkbox[1]"] = "A" if use_interpreter == "no" else "Off"

    if use_preparer:
        current_form["form1[0].Page4[0].Part3_Checkbox[0]"] = "C" if use_preparer == "yes" else "Off"

    if daytime_tel:
        current_form["form1[0].Page4[0].Pt3Line3_DaytimePhoneNumber1[0]"] = daytime_tel
    
    if mobile_tel:
        current_form["form1[0].Page4[0].Pt3Line4_MobileNumber1[0]"] = mobile_tel

    if email_addr:
        current_form["form1[0].Page4[0].Pt3Line5_Email[0]"] = email_addr

    if is_salva_guate:
        current_form["form1[0].Page4[0].Pt4Line6_Checkbox[0]"] = "A" if is_salva_guate == "yes" else "Off"

    if sign_date:
        current_form["form1[0].Page4[0].Pt3Line7b_DateofSignature[0]"] = sign_date

    utils.write_json_and_pdf_form(current_form, json_file_current_form)

    return "Complete"

def set_i765_interpreter(family_name=None, given_name=None, business_org=None, street=None, res_cat=None, city_town=None, state=None, zip_code=None, province=None, postal_code=None, country=None, daytime_tel=None, mobile_tel=None, email_addr=None, fluent_lang=None, sign_date=None):
    current_form = utils.read_json_current_form(json_file_current_form=json_file_current_form)

    if family_name:
        current_form["form1[0].Page4[0].Pt4Line1a_InterpreterFamilyName[0]"] = family_name
    
    if given_name:
        current_form["form1[0].Page4[0].Pt4Line1b_InterpreterGivenName[0]"] = given_name

    if business_org:
        current_form["form1[0].Page4[0].Pt4Line2_InterpreterBusinessorOrg[0]"] = business_org

    if street:
        current_form["form1[0].Page5[0].Pt5Line3a_StreetNumberName[0]"] = street

    if res_cat:
        current_form["form1[0].Page5[0].Pt5Line3b_Unit[0]"] = "Off"
        current_form["form1[0].Page5[0].Pt5Line3b_Unit[1]"] = "Off"
        current_form["form1[0].Page5[0].Pt5Line3b_Unit[2]"] = "Off"

        if res_cat["cat"] == "ste":
            current_form["form1[0].Page5[0].Pt5Line3b_Unit[0]"] = " STE "
        elif res_cat["cat"] == "flr":
            current_form["form1[0].Page5[0].Pt5Line3b_Unit[1]"] = " FLR "
        elif res_cat["cat"] == "apt":
            current_form["form1[0].Page5[0].Pt5Line3b_Unit[2]"] = " APT "
        else:
            pass

        current_form["form1[0].Page5[0].Pt5Line3b_AptSteFlrNumber[0]"] = res_cat.get("name", "")

    if city_town:
        current_form["form1[0].Page5[0].Pt5Line3c_CityOrTown[0]"] = city_town

    if state:
        current_form["form1[0].Page5[0].Pt5Line3d_State[0]"] = state

    if zip_code:
        current_form["form1[0].Page5[0].Pt5Line3e_ZipCode[0]"] = zip_code

    if province:
        current_form["form1[0].Page5[0].Pt5Line3f_Province[0]"] = province

    if postal_code:
        current_form["form1[0].Page5[0].Pt5Line3g_PostalCode[0]"] = postal_code

    if country:
        current_form["form1[0].Page5[0].Pt5Line3h_Country[0]"] = country

    if daytime_tel:
        current_form["form1[0].Page5[0].Pt4Line4_InterpreterDaytimeTelephone[0]"] = daytime_tel

    if mobile_tel:
        current_form["form1[0].Page5[0].Pt4Line5_MobileNumber[0]"] = mobile_tel

    if email_addr:
        current_form["form1[0].Page5[0].Pt4Line6_Email[0]"] = email_addr

    if fluent_lang:
        current_form["form1[0].Page5[0].Part4_NameofLanguage[0]"] = fluent_lang

    if sign_date:
        current_form["form1[0].Page5[0].Pt4Line6b_DateofSignature[0]"] = sign_date

    utils.write_json_and_pdf_form(current_form, json_file_current_form)

    return "Complete"

def set_i765_preparer(family_name=None, given_name=None, business_org=None, street=None, res_cat=None, city_town=None, state=None, zip_code=None, province=None, postal_code=None, country=None, daytime_tel=None, mobile_tel=None, email_addr=None, is_attorney=None, sign_date=None):
    current_form = utils.read_json_current_form(json_file_current_form=json_file_current_form)

    if family_name:
        current_form["form1[0].Page5[0].Pt5Line1a_PreparerFamilyName[0]"] = family_name
    
    if given_name:
        current_form["form1[0].Page5[0].Pt5Line1b_PreparerGivenName[0]"] = given_name

    if business_org:
        current_form["form1[0].Page5[0].Pt5Line2_BusinessName[0]"] = business_org

    if street:
        current_form["form1[0].Page5[0].Pt6Line3a_StreetNumberName[0]"] = street

    if res_cat:
        current_form["form1[0].Page5[0].Pt6Line3b_Unit[0]"] = "Off"
        current_form["form1[0].Page5[0].Pt6Line3b_Unit[1]"] = "Off"
        current_form["form1[0].Page5[0].Pt6Line3b_Unit[2]"] = "Off"

        if res_cat["cat"] == "ste":
            current_form["form1[0].Page5[0].Pt6Line3b_Unit[0]"] = " STE "
        elif res_cat["cat"] == "flr":
            current_form["form1[0].Page5[0].Pt6Line3b_Unit[1]"] = " FLR "
        elif res_cat["cat"] == "apt":
            current_form["form1[0].Page5[0].Pt6Line3b_Unit[2]"] = " APT "
        else:
            pass

        current_form["form1[0].Page5[0].Pt6Line3b_AptSteFlrNumber[0]"] = res_cat.get("name", "")

    if city_town:
        current_form["form1[0].Page5[0].Pt6Line3c_CityOrTown[0]"] = city_town

    if state:
        current_form["form1[0].Page5[0].Pt6Line3d_State[0]"] = state

    if zip_code:
        current_form["form1[0].Page5[0].Pt6Line3e_ZipCode[0]"] = zip_code

    if province:
        current_form["form1[0].Page5[0].Pt6Line3f_Province[0]"] = province

    if postal_code:
        current_form["form1[0].Page5[0].Pt6Line3g_PostalCode[0]"] = postal_code

    if country:
        current_form["form1[0].Page5[0].Pt6Line3h_Country[0]"] = country

    if daytime_tel:
        current_form["form1[0].Page5[0].Pt5Line4_DaytimePhoneNumber1[0]"] = daytime_tel

    if mobile_tel:
        current_form["form1[0].Page5[0].Pt5Line5_PreparerFaxNumber[0]"] = mobile_tel

    if email_addr:
        current_form["form1[0].Page5[0].Pt5Line6_Email[0]"] = email_addr

    if is_attorney:
        current_form["form1[0].Page6[0].Part5Line7_Checkbox[0]"] = "A" if is_attorney.get("attorney") == "no" else "Off"
        current_form["form1[0].Page6[0].Part5Line7_Checkbox[1]"] = "B" if is_attorney.get("attorney") == "yes" else "Off"

        if is_attorney.get("attorney") == "yes":
            current_form["form1[0].Page6[0].Part5Line7b_Checkbox[0]"] = "Y" if is_attorney.get("extend") == "yes" else "Off"
            current_form["form1[0].Page6[0].Part5Line7b_Checkbox[1]"] = "N" if is_attorney.get("extend") == "no" else "Off"

    if sign_date:
        current_form["form1[0].Page6[0].Pt5Line8b_DateofSignature[0]"] = sign_date

    utils.write_json_and_pdf_form(current_form, json_file_current_form)

    return "Complete"

custom_tools = [
    {
        "type": "function",
        "function": {
            "name": "set_i765_1st_page",
            "description": """Fill the page 1 of the I-765 form. 
                The user will enter relevant information including reason for the application (reason), full legal names (legal names), G28 form attachment (is_g28_attached), or USCIS online account number (uscis_online_account_number).
                The user may inform only one or more variables per query.
                """,
            "parameters": {
                "type": "object",
                "required": [],
                "properties": {
                    "reason": {
                        "type": "string",
                        "description": "The part 1 of I-765. The user will tell the reason for the application.",
                        "enum": ["initial", "replace", "renewal"]
                    },
                    "legal_names": {
                        "type": "object",
                        "description": """The part 2 of I-765. The user's full legal name as the first and then the name ever used including aliases, maiden name, and nicknames. 
                            For example, the current name is Josh Bold Baron and the previous name was Graham Belle. So, get {'1': 'Josh Bold Baron', '2': 'Graham Belle'}""",
                    },
                    "is_g28_attached": {
                        "type": "string",
                        "description": "'yes' if the G-28 form is attached for the application. Otherwise, 'no'",
                        "enum": ["yes", "no"]
                    },
                    "uscis_online_account_number": {
                        "type": "string",
                        "description": "Attorney or Accredited Representative USCIS Online Account Number (if any). This must be 12 digits. If don't have this number, let it blank."
                    }
                }
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_i765_2nd_page_us_mail_addr",
            "description": """Fill the user's US Mailing Address in the page 2 of the I-765 form.
                The user may inform one or more variables per query.
                The user will enter the U.S. Mailing Address details may including:
                - In Care Of Name (if any)
                - Street Number and Name
                - Apartment, Suite, or Floor
                - City or Town
                - State
                - Zip code
                - Is your current mailing address the same as your physical address?
                """,
            "parameters": {
                "type": "object",
                "required": [],
                "properties": {
                    "in_care_of_name": {
                        "type": "string",
                        "description": "In care of name (c/o) in the U.S. Mailing Address.",
                    },
                    "street": {
                        "type": "string",
                        "description": "Street number and name such as, '123, Main Street'",
                    },
                    "res_cat": {
                        "type": "object",
                        "description": """
                            One of the 3 categories of the residence only including 'apt' for apartment, 'flr' for floor, and 'ste' for suite with its name.
                            For example, Apt. Chamber to {'cat': 'apt', 'name': 'Chamber'} (it is dictionary not string), Flr. 11 to {'cat': 'flr', 'name': '11'}  (it is dictionary not string)
                            """,
                    },
                    "city_town": {
                        "type": "string",
                        "description": "City or town name."
                    },
                    "state": {
                        "type": "string",
                        "description": "State of the mailing address such as 'AK' for Alaska, 'AZ' for Arizona",
                        "enum": [
                            "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL",
                            "IN", "IA", "KS", "KY", "LA", "ME", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC",
                            "ND", "OH", "OK", "OR", "MD", "MA", "MI", "MN", "MS", "MO", "PA", "RI", "SC", "SD",
                            "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
                        ]
                    },
                    "zip_code": {
                        "type": "string",
                        "description": "Zip code corresponding to state and city such as '31905'"
                    },
                    "is_same_physical": {
                        "type": "string",
                        "description": "Is your current mailing address the same as your physical address?",
                        "enum": ["yes", "no"]
                    }
                }
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_i765_2nd_page_us_physic_addr",
            "description": """Fill the user's US Physical Address in the page 2 of the I-765 form.
                The user may inform only one or more variables per query.
                The user will enter the U.S. Physical Address details may including:
                - Street Number and Name
                - Apartment, Suite, or Floor
                - City or Town
                - State
                - Zip code
                """,
            "parameters": {
                "type": "object",
                "required": [],
                "properties": {
                    "street": {
                        "type": "string",
                        "description": "Street number and name such as, '123, Main Street'",
                    },
                    "res_cat": {
                        "type": "object",
                        "description": """
                            One of the 3 categories of the residence only including 'apt' for apartment, 'flr' for floor, and 'ste' for suite with its name.
                            For example, Apt. Chamber to {'cat': 'apt', 'name': 'Chamber'}, Flr. 11 to {'cat': 'flr', 'name': '11'}
                            """,
                    },
                    "city_town": {
                        "type": "string",
                        "description": "City or town name."
                    },
                    "state": {
                        "type": "string",
                        "description": "State of the mailing address such as 'AK' for Alaska, 'AZ' for Arizona",
                        "enum": [
                            "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL",
                            "IN", "IA", "KS", "KY", "LA", "ME", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC",
                            "ND", "OH", "OK", "OR", "MD", "MA", "MI", "MN", "MS", "MO", "PA", "RI", "SC", "SD",
                            "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
                        ]
                    },
                    "zip_code": {
                        "type": "string",
                        "description": "Zip code corresponding to state and city such as '31905'"
                    },
                }
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_i765_2nd_page_personal_info",
            "description": """Fill the user's personal information in the page 2 of the I-765 form.
                The user may inform only one or more variables per query.
                The user will enter the details may including:
                - Alien Registration Number (A-Number) (if any)
                - USCIS Online Account Number (if any)
                - Gender
                - Marital Status
                - Have you previously filed Form I-765?
                - Receive Social Security card?
                - SSA to issue you a Social Security card?
                - disclosure of information from this application to the SSA?
                - Father's name
                - Mother's name
                - Countries of citizenship
                """,
            "parameters": {
                "type": "object",
                "required": [],
                "properties": {
                    "a_number": {
                        "type": "string",
                        "description": """Alien Registration Number (A-Number) (if any). 
                            For example, 'A-123456789' should get '123456789'""",
                    },
                    "uscis_online_account_number": {
                        "type": "string",
                        "description": "Attorney or Accredited Representative USCIS Online Account Number (if any). This must be 12 digits."
                    },
                    "gender": {
                        "type": "string",
                        "description": "Gender of the user",
                        "enum": ["male", "female"]
                    },
                    "marital_status": {
                        "type": "string",
                        "description": "Marital status of the user.",
                        "enum": ["single", "married", "divorced", "widowed"]
                    },
                    "filed_i765_before": {
                        "type": "string",
                        "description": "Have the user previously filed Form I-765?",
                        "enum": ["yes", "no"]
                    },
                    "ssc": {
                        "type": "object",
                        "description": """
                            Has the Social Security Administration (SSA) ever officially issued a Social Security card? 
                            If yes, provide Social Security number (SSN) (if known).
                            For example, if yes and SSN is 123456789 then ssc={'card': 'yes', 'ssn': '123456789'}, if no, then ssc={'card': 'no'}
                            """
                    },
                    "issue_ssc": {
                        "type": "object",
                        "description": """
                            Do the user want the SSA to issue you a Social Security card?
                            1. 'no' then issue_ssc={'issue': 'no'}
                            2. 'yes' then ask the user about Consent for Disclosure?
                            2.1 'no' then issue_ssc={'issue': 'yes', 'disc': 'no'}
                            2.2 'yes' then issue_ssc={'issue': 'yes', 'disc': 'yes'}
                        """
                    },
                    "father_name": {
                        "type": "string",
                        "description": "Full name of the user's father."
                    },
                    "mother_name": {
                        "type": "string",
                        "description": "Full name of the user's mother."
                    },
                    "citizenship": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "minItems": 1,
                        "maxItems": 2,
                        "description": "The user's countries of citizenship or nationality. For example ['Canada', 'Mexico']"
                    }
                }
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_i765_3rd_page_place_birth",
            "description": """Fill the personal information about the birth place in the third page of the I-765 form.
                The user may inform only one or more variables per query.
                The user will enter the details may including:
                - City/Town/Village of Birth
                - State/Province of Birth
                - Country of Birth
                - Date of Birth
                """,
            "parameters": {
                "type": "object",
                "required": [],
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City/Town/Village of Birth of the user.",
                    },
                    "state": {
                        "type": "string",
                        "description": "State/Province of Birth of the user."
                    },
                    "country": {
                        "type": "string",
                        "description": "Country of Birth of the user",
                    },
                    "dob": {
                        "type": "string",
                        "description": "Date of Birth of the user. The date format is mm/dd/yyyy such as 07/19/1999",
                    }
                }
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_i765_3rd_page_last_us_arrival",
            "description": """Fill the information about the last arrival in the US. in the thrid page of the I-765 form.
                The user may inform only one or more variables per query.
                The user will enter the details may including:
                - Form I-94 Arrival-Departure Record Number (if any)
                - Passport Number of Your Most Recently Issued Passport
                - Travel Document Number (if any)
                - Country That Issued Your Passport or Travel Document
                - Expiration Date for Passport or Travel Document
                - Date of Your Last Arrival Into the United States, On or About
                - Place of Your Last Arrival Into the United States
                - Immigration Status at Your Last Arrival
                - Your Current Immigration Status or Category
                - Student and Exchange Visitor Information System (SEVIS) Number (if any)
                """,
            "parameters": {
                "type": "object",
                "required": [],
                "properties": {
                    "arr_dep_num": {
                        "type": "string",
                        "description": "Form I-94 Arrival-Departure Record Number (if any) should be 11 digits.",
                    },
                    "pass_num": {
                        "type": "string",
                        "description": "Passport Number of Your Most Recently Issued Passport."
                    },
                    "trav_doc_num": {
                        "type": "string",
                        "description": "Travel Document Number (if any).",
                    },
                    "country_issue": {
                        "type": "string",
                        "description": "Country That Issued Your Passport or Travel Document.",
                    },
                    "exp_date": {
                        "type": "string",
                        "description": "Expiration Date for Passport or Travel Document. The date format is mm/dd/yyyy such as 07/19/1999",
                    },
                    "last_date_us": {
                        "type": "string",
                        "description": "Date of Your Last Arrival Into the United States, On or About. The date format is mm/dd/yyyy such as 07/19/1999",
                    },
                    "last_place_us": {
                        "type": "string",
                        "description": "Place of Your Last Arrival Into the United States",
                    },
                    "immg_status_last_arr": {
                        "type": "string",
                        "description": "Immigration Status at Your Last Arrival. (for example, B-2 visitor, F-1 student, or no status)",
                    },
                    "cur_immg_status": {
                        "type": "string",
                        "description": "Your Current Immigration Status or Category. (for example, B-2 visitor, F-1 student, parolee, deferred action, or no status or category)",
                    },
                    "sevis": {
                        "type": "string",
                        "description": "Student and Exchange Visitor Information System (SEVIS) Number (if any), such as 'N-1234567' to be '1234567'"
                    },
                }
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_i765_3rd_page_elig_cat",
            "description": """Fill the information about eligibility category in the thrid page of the I-765 form.
                The user may inform only one or more variables per query.
                The user will enter the details may including:
                - Eligibility Category: Refer to the Who May File Form I-765 section of the Form I-765 Instructions
                - (c)(3)(C) STEM OPT Eligibility Category
                - (c)(26) Eligibility Category
                - (c)(8) Eligibility Category
                - (c)(35) and (c)(36) Eligibility Category
                """,
            "parameters": {
                "type": "object",
                "required": [],
                "properties": {
                    "elig_cat": {
                        "type": "string",
                        "description": "Item number 27. Eligibility Category. Refer to the Who May File Form I-765 section of the Form I-765 Instructions to determine the appropriate eligibility category for this application. (for example, '(a)(8)', or '(c)(17)(iii)')"
                    },
                    "c3c_stem": {
                        "type": "object",
                        "description": """If you entered the eligibility category (c)(3)(C) in Item Number 27., provide the information including Degree, Employer's Name as Listed in E-Verify (emp_name), and Employer's E-Verify Company Identification Number or a Valid E-Verify Client Company Identification Number
                                    For example {"degree": "bachelor", "emp_name": "Mike Johnson", "e_verify": "1234567"}
                                    """
                    },
                    "c26": {
                        "type": "string",
                        "description": "If you entered the eligibility category (c)(26) in Item Number 27., provide the receipt number of your H-1B spouse's most recent Form I-797 Notice for Form I-129, Petition for a Nonimmigrant Worker. This must be 13 digits.",
                    },
                    "c8": {
                        "type": "string",
                        "description": "If you entered the eligibility category (c)(8) in Item Number 27., have you EVER been arrested for and/or convicted of any crime?",
                        "enum": ["yes", "no"],
                    },
                    "c35_c36": {
                        "type": "object",
                        "description": """Provide 2 things:
                                        1. The receipt number (rec_num) (13 digits):
                                        - If you entered the eligibility category (c)(35) in Item Number 27., please provide the receipt number of your Form I-797 Notice for Form I-140. 
                                        - If you entered the eligibility category (c)(36) in Item Number 27., please provide the receipt number of your spouse's or parent's Form I-797 Notice for Form I-140.,
                                        2. Have you EVER been arrested for and/or convicted of any crime? (crime) (ans: yes/no).
                                        
                                        For example, give answer like this pattern: {'rec_num': '1234567890123', 'crime': 'no'}
                                        """
                    },
                }
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_i765_4th_page_applicant",
            "description": """Fill the applicant information in the fourth page of the I-765 form.
                The user may inform only one or more variables per query.
                The user will enter the details may including:
                - Did the user use interpreter?
                - Did the user use preparer?
                - Daytime Telephone Number
                - Mobile Telephone Number (if any)
                - Email Address (if any)
                - Is the user Salvadoran or Guatemalan?
                - Signature date
                """,
            "parameters": {
                "type": "object",
                "required": [],
                "properties": {
                    "use_interpreter": {
                        "type": "string",
                        "description": "Did the user use interpreter? If no, means the user can read and understand English, and the user have read and understand every question and instruction on this application and my answer to every question.",
                        "enum": ["yes", "no"],
                    },
                    "use_preparer": {
                        "type": "string",
                        "description": "Did the user use preparer? If yes, means the preparer prepared this application for the user based only upon information provided or authorized.",
                        "enum": ["yes", "no"],
                    },
                    "daytime_tel": {
                        "type": "string",
                        "description": "Applicant's Daytime Telephone Number.",
                    },
                    "mobile_tel": {
                        "type": "string",
                        "description": "Applicant's Mobile Telephone Number (if any).",
                    },
                    "email_addr": {
                        "type": "string",
                        "description": "Applicant's Email Address (if any).",
                    },
                    "is_salva_guate": {
                        "type": "string",
                        "description": "Is the user Salvadoran or Guatemalan?",
                        "enum": ["yes", "no"],
                    },
                    "sign_date": {
                        "type": "string",
                        "description": "Date of Applicant's Signature. The format date is mm/dd/yyyy"
                    },
                }
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_i765_interpreter",
            "description": """Fill the interpreter information of the I-765 form.
                The user may inform only one or more variables per query.
                The user will enter the details may including:
                - Interpreter's Family Name (Last Name)
                - Interpreter's Given Name (First Name)
                - Interpreter's Business or Organization Name (if any)
                - Interpreter's Mailing Address
                - Interpreter's Daytime Telephone Number
                - Interpreter's Mobile Telephone Number (if any)
                - Interpreter's Email Address (if any)
                - Interpreter's Fluent Language
                - Interpreter's Date of Signature
                """,
            "parameters": {
                "type": "object",
                "required": [],
                "properties": {
                    "family_name": {
                        "type": "string",
                        "description": "Interpreter's Family Name (Last Name).",
                    },
                    "given_name": {
                        "type": "string",
                        "description": "Interpreter's Given Name (First Name).",
                    },
                    "business_org": {
                        "type": "string",
                        "description": "Interpreter's Business or Organization Name (if any).",
                    },
                    "street": {
                        "type": "string",
                        "description": "Interpreter's Mailing Address: Street number and name such as, '123, Main Street'",
                    },
                    "res_cat": {
                        "type": "object",
                        "description": """
                            Interpreter's Mailing Address: 
                            One of the 3 categories of the residence only including 'apt' for apartment, 'flr' for floor, and 'ste' for suite with its name.
                            For example, Apt. Chamber to {'cat': 'apt', 'name': 'Chamber'}, Flr. 11 to {'cat': 'flr', 'name': '11'}
                            """,
                    },
                    "city_town": {
                        "type": "string",
                        "description": "Interpreter's Mailing Address: City or town name."
                    },
                    "state": {
                        "type": "string",
                        "description": "Interpreter's Mailing Address: State of the mailing address such as 'AK' for Alaska, 'AZ' for Arizona",
                        "enum": [
                            "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL",
                            "IN", "IA", "KS", "KY", "LA", "ME", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC",
                            "ND", "OH", "OK", "OR", "MD", "MA", "MI", "MN", "MS", "MO", "PA", "RI", "SC", "SD",
                            "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
                        ]
                    },
                    "zip_code": {
                        "type": "string",
                        "description": "Interpreter's Mailing Address: Zip code corresponding to state and city such as '31905. Primarily uses in the United States and the Philippines."
                    },
                    "province": {
                        "type": "string",
                        "description": "Interpreter's Mailing Address: Province."
                    },
                    "postal_code": {
                        "type": "string",
                        "description": "Interpreter's Mailing Address: Postal code corresponding to the province"
                    },
                    "country": {
                        "type": "string",
                        "description": "Interpreter's Mailing Address: Country"
                    },
                    "daytime_tel": {
                        "type": "string",
                        "description": "Interpreter's Daytime Telephone Number.",
                    },
                    "mobile_tel": {
                        "type": "string",
                        "description": "Interpreter's Mobile Telephone Number (if any).",
                    },
                    "email_addr": {
                        "type": "string",
                        "description": "Interpreter's Email Address (if any).",
                    },
                    "fluent_lang": {
                        "type": "string",
                        "description": "Interpreter's fluent language which is not English.",
                    },
                    "sign_date": {
                        "type": "string",
                        "description": "Date of Interpreter's Signature. The format date is mm/dd/yyyy"
                    },
                }
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_i765_preparer",
            "description": """Fill the preparer information of the I-765 form.
                The user may inform only one or more variables per query.
                The user will enter the details may including:
                - Preparer's Family Name (Last Name)
                - Preparer's Given Name (First Name)
                - Preparer's Business or Organization Name (if any)
                - Preparer's Mailing Address
                - Preparer's Daytime Telephone Number
                - Preparer's Mobile Telephone Number (if any)
                - Preparer's Email Address (if any)
                - Is preparer an attorney?
                - Preparer's Date of Signature
                """,
            "parameters": {
                "type": "object",
                "required": [],
                "properties": {
                    "family_name": {
                        "type": "string",
                        "description": "Preparer's Family Name (Last Name).",
                    },
                    "given_name": {
                        "type": "string",
                        "description": "Preparer's Given Name (First Name).",
                    },
                    "business_org": {
                        "type": "string",
                        "description": "Preparer's Business or Organization Name (if any).",
                    },
                    "street": {
                        "type": "string",
                        "description": "Preparer's Mailing Address: Street number and name such as, '123, Main Street'",
                    },
                    "res_cat": {
                        "type": "object",
                        "description": """
                            Preparer's Mailing Address: 
                            One of the 3 categories of the residence only including 'apt' for apartment, 'flr' for floor, and 'ste' for suite with its name.
                            For example, Apt. Chamber to {'cat': 'apt', 'name': 'Chamber'}, Flr. 11 to {'cat': 'flr', 'name': '11'}
                            """,
                    },
                    "city_town": {
                        "type": "string",
                        "description": "Preparer's Mailing Address: City or town name."
                    },
                    "state": {
                        "type": "string",
                        "description": "Preparer's Mailing Address: State of the mailing address such as 'AK' for Alaska, 'AZ' for Arizona",
                        "enum": [
                            "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL",
                            "IN", "IA", "KS", "KY", "LA", "ME", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC",
                            "ND", "OH", "OK", "OR", "MD", "MA", "MI", "MN", "MS", "MO", "PA", "RI", "SC", "SD",
                            "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
                        ]
                    },
                    "zip_code": {
                        "type": "string",
                        "description": "Preparer's Mailing Address: Zip code corresponding to state and city such as '31905. Primarily uses in the United States and the Philippines."
                    },
                    "province": {
                        "type": "string",
                        "description": "Preparer's Mailing Address: Province."
                    },
                    "postal_code": {
                        "type": "string",
                        "description": "Preparer's Mailing Address: Postal code corresponding to the province"
                    },
                    "country": {
                        "type": "string",
                        "description": "Preparer's Mailing Address: Country"
                    },
                    "daytime_tel": {
                        "type": "string",
                        "description": "Preparer's Daytime Telephone Number.",
                    },
                    "mobile_tel": {
                        "type": "string",
                        "description": "Preparer's Mobile Telephone Number (if any).",
                    },
                    "email_addr": {
                        "type": "string",
                        "description": "Preparer's Email Address (if any).",
                    },
                    "is_attorney": {
                        "type": "object",
                        "description": """Is the preparer an attorney or accredited representative? 
                                        If yes, then do the application extend beyond the preparation of the application?
                                        For example,
                                        - The preparer isn't an attorney: {'attorney': 'no'}
                                        - The preparer isn't an attorney, but doesn't extend beyond the preparation: {'attorney': 'yes', 'extend': 'no'}
                                        """, 
                    },
                    "sign_date": {
                        "type": "string",
                        "description": "Date of Preparer's Signature. The format date is mm/dd/yyyy"
                    },
                }
            },
        }
    },
]

system_prompt = """
You are an immigration officer experienced in helping applicants fill out the I-765 form for Employment Authorization. 
The I-765 form contains 7 pages, but you and the user must focus only first 6 pages. The seventh page isn't important. So, don't need to advice anything.
Your job is to guide me through each section of the form and ask me for the information needed. 
Start by asking for my information according to the first page of the form, and then go page-by-page and section-by-section to ensure everything is filled out accurately. 
If there’s a specific category or option I should choose, provide me with recommendations based on typical guidelines. 

These pages contain in the I-765 form:
Page 1:
- G28: Is the user attached the G28 form?
- USCIS Online Account Number: Attorney or Accredited Representative USCIS Online Account Number (if any) (12 digits)
- Reason for application: Either Initial permission, Replace the previous, or Renewal the permission
- Full legal name: The user's full legal name and the previous name including aliases, maiden name, and nicknames.

Page 2:
- U.S. Mailing Address: includes In Care Of Name (if any), Street number and name, Apt. Ste. Flr. and name, City or Town, State, Zip code, and Is your current mailing address the same as your physical address? (if yes, just skip the physical address)
- U.S. Physical Address: includes Street number and name, Apt. Ste. Flr. and name, City or Town, State, Zip code
- Personal information: includes Alien Registration Number (A-Number) (if any), USCIS Online Account Number (if any), Gender, Marital Status, Have you previously filed Form I-765?, Receive Social Security card? if yes, the user may tell the card ID, SSA to issue you a Social Security card?, disclosure of information from this application to the SSA? if yes, ask for both Father's name and Mother's name, Countries of citizenship

Page 3:
- Place of Birth: includes List the city/town/village, state/province, and country where you were born, and the date of birth.
- Information About Your Last Arrival in the United States: includes Arrival-Departure Record Number (if any), Passport Number of Your Most Recently Issued Passport, Travel Document Number (if any), Country That Issued Your Passport or Travel Document, Expiration Date for Passport or Travel Document, Date of Your Last Arrival Into the United States, Place of Your Last Arrival Into the United States, Immigration Status at Your Last Arrival (for example, B-2 visitor, F-1 student, or no status), Your Current Immigration Status or Category (for example, B-2 visitor, F-1 student, parolee, deferred action, or no status or category), Student and Exchange Visitor Information System (SEVIS) Number (if any), 
- Information About Your Eligibility Category: Eligibility Category (Item number 27. Refer to the Who May File Form I-765 section).
    1. if (c)(3)(C) is referred in the Eligibility Category, the (c)(3)(C) STEM OPT Eligibility Category is a must (includes Degree, Employer's Name as Listed in E-Verify, Employer's E-Verify Company Identification Number or a Valid E-Verify Client Company Identification Number)
    2. if (c)(26) is referred in the Eligibility Category, must do (c)(26) Eligibility Category
    3. if (c)(26) is referred in the Eligibility Category, (c)(8) Eligibility Category is a must
    4. if (c)(35) or (c)(36) is referred in the Eligibility Category, (c)(35) and (c)(36) Eligibility Category is a must

Page 4:
- Applicant's Statement: includes 
    1) choosing either capability to read and understand English, and read and understand every question and instruction (1.a.) or using interpreter named in Part 4. read to me every question and instruction on this application (1.b.)
    2) choosing to admit that the preparer named in Part 5., prepared this application for the user
- Applicant's Signature: includes the user's signature (cannot edit in here) and Date of Signature (mm/dd/yyyy) (available here)
- Interpreter's Full Name: includes the interpreter's family and given name and the interpreter's Business or Organization Name

Page 5:
- Interpreter's Contact Information, Certification, and Signature: Interpreter's Mailing Address, Interpreter's Contact Information (Daytime Telephone Number, Mobile Telephone Number (if any), Email Address (if any)), A fluent language, date of signature
- Contact Information, Declaration, and Signature of the Person Preparing this Application, If Other Than the Applicant: Preparer's Full Name, Preparer's Mailing Address, Preparer's Contact Information (Daytime Telephone Number, Mobile Telephone Number (if any), Email Address (if any))

Page 6:
- Contact Information, Declaration, and Signature of the Person Preparing this Application, If Other Than the Applicant (continued): Preparer's Statement (about preparer being attorney), date of signature

Page 7:
- Additional Information: If you need extra space to provide any additional information within this application, use this page.

Assignment:
- Please show what you get to the user before filling the PDF form
- Before going to a next page, please inform the user what are filled and ask the user's before
- If the user ask for other forms, then replies 'no, only support I-765'
- If the user talk about other things, replies 'I am here for immigration and help filling the I-765 form only'
"""

system_message = [{"role": "system", "content": system_prompt}]

def reply_prompt(messages, together_api_key):
    client = openai.OpenAI(
        base_url="https://api.together.xyz/v1",
        api_key=together_api_key,
    )

    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        messages=system_message + messages[-10:], # Conversation history
        stream=False,
        tools=custom_tools, # Available tools (i.e. functions) for our LLM to use
        tool_choice="auto", # Let our LLM decide when to use tools
        max_tokens=500, # Maximum number of tokens to allow in our response
        temperature=0,
    )

    # Extract the response and any tool call responses
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    print("tool_calls", tool_calls)

    if tool_calls:
        # Define the available tools that can be called by the LLM
        available_functions = {
            "set_i765_1st_page": set_i765_1st_page,
            "set_i765_2nd_page_us_mail_addr": set_i765_2nd_page_us_mail_addr,
            "set_i765_2nd_page_us_physic_addr": set_i765_2nd_page_us_physic_addr,
            "set_i765_2nd_page_personal_info": set_i765_2nd_page_personal_info,
            "set_i765_3rd_page_place_birth": set_i765_3rd_page_place_birth,
            "set_i765_3rd_page_last_us_arrival": set_i765_3rd_page_last_us_arrival,
            "set_i765_3rd_page_elig_cat": set_i765_3rd_page_elig_cat,
            "set_i765_4th_page_applicant": set_i765_4th_page_applicant,
            "set_i765_interpreter": set_i765_interpreter,
            "set_i765_preparer": set_i765_preparer
        }

        # Add the LLM's response to the conversation
        messages.append(response_message)

        # Process each tool call
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)

            print("function_name", function_name)
            print("function_to_call", function_to_call)
            print("function_args", function_args)

            # Call the tool and get the response
            function_response = function_to_call(**function_args)

            # Add the tool response to the conversation
            messages.append(
                {
                    "tool_call_id": tool_call.id, 
                    "role": "tool", # Indicates this message is from tool use
                    "name": function_name,
                    "content": function_response,
                }
            )

        response_stream = client.chat.completions.create(
            model=model,
            messages=system_message + messages[-10:],
            stream=True,
            max_tokens=500,
        )

        return response_stream
    
    else:
        # No functions called
        response_stream = client.chat.completions.create(
            model=model,
            messages=system_message + messages[-10:],
            stream=True,
            max_tokens=500,
        )

        return response_stream



# system_prompt = """You are an expert in composing functions. You are given a question and a set of possible functions. 
# Based on the question, you will need to make one or more function/tool calls to achieve the purpose. 
# If none of the function can be used, point it out. If the given question lacks the parameters required by the function,
# also point it out. You should only return the function call in tools call sections.

# If you decide to invoke any of the function(s), you MUST put it in the format of [func_name1(params_name1=params_value1, params_name2=params_value2...), func_name2(params)]\n
# You SHOULD NOT include any other text in the response.

# Here is a list of functions in JSON format that you can invoke.\n\n{functions}\n""".format(functions=function_definitions)
