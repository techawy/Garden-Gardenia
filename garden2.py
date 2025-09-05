import streamlit as st
from streamlit.components.v1 import html
import google.generativeai as genai
from streamlit_chat import message
from googlesearch import search
import requests as req
import random
import json
from datetime import datetime, timedelta
import pandas as pd
import calendar

APP_VERSION = "4.0"

def initialize_session_state():
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []
    if 'weather_data' not in st.session_state:
        st.session_state['weather_data'] = None
    if 'plant_disease_data' not in st.session_state:
        st.session_state['plant_disease_data'] = None
    if 'theme' not in st.session_state:
        st.session_state['theme'] = 'nature_green'
    if 'language' not in st.session_state:
        st.session_state['language'] = 'English'
    if 'animation_style' not in st.session_state:
        st.session_state['animation_style'] = 'floating_leaves'
    if 'text_animation' not in st.session_state:
        st.session_state['text_animation'] = 'typewriter'
    if 'editing_index' not in st.session_state:
        st.session_state['editing_index'] = None
    if 'edit_text' not in st.session_state:
        st.session_state['edit_text'] = ""
    if 'show_info' not in st.session_state:
        st.session_state['show_info'] = False
    if 'show_settings' not in st.session_state:
        st.session_state['show_settings'] = False
    if 'watering_schedules' not in st.session_state:
        st.session_state['watering_schedules'] = []
    if 'garden_journals' not in st.session_state:
        st.session_state['garden_journals'] = []
    if 'selected_plants' not in st.session_state:
        st.session_state['selected_plants'] = []

initialize_session_state()

try:
    genai.configure(api_key="AIzaSyA5RMHXOoVasqXObWwTZwusBqG1y9Cihtk")
    model = genai.GenerativeModel('gemini-2.0-flash-lite')
except Exception as e:
    st.error(f"Failed to initialize AI model: {str(e)}")

translations = {
    'English': {
        "title": "Smart Garden Planning System",
        "section1": "Garden Dimensions",
        "section2": "Soil and Weather Information",
        "section3": "Planting Suggestions",
        "section4": "Plant Disease Diagnosis",
        "section5": "Smart Garden Assistant",
        "section6": "Watering Schedule",
        "section7": "Garden Journal",
        "unit": "Measurement Unit:",
        "units": ['meter', 'kilometer', 'acre', 'hectare'],
        "area": "Area:",
        "country": "Country:",
        "city": "City:",
        "soil": "Soil Type:",
        "soils": ['Clay', 'Loamy', 'Sandy', 'Silty', 'Peaty', 'Chalky'],
        "crops": "Desired Crops:",
        "analyze": "Analyze Crops",
        "plant_symptoms": "Plant Symptoms:",
        "plant_type": "Plant Type:",
        "diagnose": "Diagnose Disease",
        "treatment": "Recommended Treatment:",
        "disease_title": "Plant Disease Diagnosis",
        "chat_title": "Smart Gardening Assistant",
        "chat_placeholder": "Ask your gardening question...",
        "search_web": "Search Web",
        "chat_response": "Assistant Response:",
        "weather_data": "Weather data for",
        "observation_time": "Observation Time:",
        "temperature": "Temperature:",
        "wind_speed": "Wind Speed:",
        "humidity": "Humidity:",
        "weather_recommendation": "Based on your city's weather data, I recommend:",
        "weather_error": "Error fetching weather data",
        "disease_error": "Diagnosis error",
        "disease_success": "Diagnosis completed successfully",
        "theme_select": "Select Theme:",
        "animation_select": "Select Animation Style:",
        "text_animation_select": "Select Text Animation:",
        "version_info": "Version Info",
        "app_version": f"Garden AI Assistant v{APP_VERSION}",
        "features": "Features",
        "feature_list": [
            "Smart garden planning system",
            "Plant disease diagnosis",
            "AI-powered gardening assistant",
            "Weather integration",
            "Multi-language support",
            "Customizable themes",
            "Editable chat history",
            "Watering schedule management",
            "Garden journal"
        ],
        "close": "Close",
        "themes": {
            "nature_green": "Nature Green",
            "ocean_blue": "Ocean Blue",
            "sunset_orange": "Sunset Orange",
            "forest_green": "Forest Green",
            "spring_blossom": "Spring Blossom",
            "custom": "Custom"
        },
        "text_animations": {
            "typewriter": "Typewriter",
            "fade_in": "Fade In",
            "slide_up": "Slide Up",
            "custom": "Custom"
        },
        "Egypt": "Egypt",
        "Cairo": "Cairo",
        "tomatoes, cucumbers, eggplants": "tomatoes, cucumbers, eggplants",
        "Yellow spots on leaves": "Yellow spots on leaves",
        "Tomato": "Tomato",
        "From growing gardens to growing mindsets": "From growing gardens to growing mindsets",
        "Analyze Current Weather": "Analyze Current Weather",
        "Generating recommendations...": "Generating recommendations...",
        "Diagnosing...": "Diagnosing...",
        "You are a plant disease specialist": "You are a plant disease specialist",
        "The affected plant is": "The affected plant is",
        "Visible symptoms are": "Visible symptoms are",
        "Please provide": "Please provide",
        "Likely diagnosis": "Likely diagnosis",
        "Possible causes": "Possible causes",
        "Recommended treatment": "Recommended treatment",
        "Prevention methods": "Prevention methods",
        "in a well-organized table": "in a well-organized table",
        "You are an agricultural consultant": "You are an agricultural consultant",
        "I need planting suggestions for": "I need planting suggestions for",
        "in": "in",
        "soil": "soil",
        "located in": "located in",
        "The garden area is": "The garden area is",
        "Current weather": "Current weather",
        "Crop name": "Crop name",
        "Soil compatibility": "Soil compatibility",
        "Weather suitability": "Weather suitability",
        "Care tips": "Care tips",
        "Here are some web resources about": "Here are some web resources about",
        "No relevant info found.": "No relevant info found.",
        "Search failed:": "Search failed:",
        "You are a smart gardening assistant": "You are a smart gardening assistant",
        "Current weather in": "Current weather in",
        "Question": "Question",
        "Please provide a detailed answer with practical tips": "Please provide a detailed answer with practical tips",
        "Error:": "Error:",
        "Select Language:": "Select Language:",
        "settings": "Settings",
        "Navigation": "Navigation",
        "watering_schedule": "Watering Schedule",
        "create_schedule": "Create Watering Schedule",
        "plant_name": "Plant Name",
        "water_frequency": "Watering Frequency (days)",
        "last_watered": "Last Watered",
        "next_watering": "Next Watering",
        "add_schedule": "Add Schedule",
        "no_schedules": "No watering schedules yet.",
        "garden_journal": "Garden Journal",
        "add_journal_entry": "Add Journal Entry",
        "journal_date": "Date",
        "journal_entry": "Journal Entry",
        "add_entry": "Add Entry",
        "no_entries": "No journal entries yet.",
        "view_journal": "View Journal",
        "view_schedule": "View Schedule",
        "delete": "Delete",
        "edit": "Edit",
        "save": "Save",
        "cancel": "Cancel",
        "confirm_delete": "Are you sure you want to delete this item?",
        "watering_reminder": "Watering Reminder",
        "due_for_watering": "The following plants are due for watering today:",
        "no_watering_due": "No plants due for watering today.",
        "journal_prompt": "What did you observe in your garden today?"
    },
    'العربية': {
        "title": "نظام التخطيط الذكي للحدائق",
        "section1": "أبعاد الحديقة",
        "section2": "معلومات التربة والطقس",
        "section3": "اقتراحات الزراعة",
        "section4": "تشخيص أمراض النباتات",
        "section5": "المساعد الذكي للحدائق",
        "section6": "جدول الري",
        "section7": "مذكرات الحديقة",
        "unit": "وحدة القياس:",
        "units": ['متر', 'كيلومتر', 'فدان', 'هكتار'],
        "area": "المساحة:",
        "country": "الدولة:",
        "city": "المدينة:",
        "soil": "نوع التربة:",
        "soils": ['طينية', 'طميية', 'رملية', 'غرينية', 'خثية', 'طباشيرية'],
        "crops": "المحاصيل المطلوبة:",
        "analyze": "تحليل المحاصيل",
        "plant_symptoms": "أعراض النبات:",
        "plant_type": "نوع النبات:",
        "diagnose": "تشخيص المرض",
        "treatment": "العلاج المقترح:",
        "disease_title": "تشخيص أمراض النباتات",
        "chat_title": "مساعد البستنة الذكي",
        "chat_placeholder": "اطرح سؤالك عن البستنة...",
        "search_web": "البحث على الإنترنت",
        "chat_response": "إجابة المساعد:",
        "weather_data": "بيانات الطقس لمدينة",
        "observation_time": "وقت المراقبة:",
        "temperature": "درجة الحرارة:",
        "wind_speed": "سرعة الرياح:",
        "humidity": "الرطوبة:",
        "weather_recommendation": "بناءً على بيانات الطقس لمدينتك، أنصح بـ:",
        "weather_error": "حدث خطأ في جلب بيانات الطقس",
        "disease_error": "حدث خطأ في التشخيص",
        "disease_success": "تم التشخيص بنجاح",
        "theme_select": "اختر المظهر:",
        "animation_select": "اختر نمط الحركة:",
        "text_animation_select": "اختر حركة النص:",
        "version_info": "معلومات النسخة",
        "app_version": f"مساعد الحديقة الذكي الإصدار {APP_VERSION}",
        "features": "المميزات",
        "feature_list": [
            "نظام تخطيط حديقة ذكي",
            "تشخيص أمراض النباتات",
            "مساعد بستنة يعمل بالذكاء الاصطناعي",
            "تكامل مع بيانات الطقس",
            "دعم متعدد اللغات",
            "سمات قابلة للتخصيص",
            "سجل محادثات قابل للتعديل",
            "إدارة جدول الري",
            "مذكرات الحديقة"
        ],
        "close": "إغلاق",
        "themes": {
            "nature_green": "أخضر طبيعي",
            "ocean_blue": "أزرق محيط",
            "sunset_orange": "برتقالي غروب",
            "forest_green": "أخضر غابة",
            "spring_blossom": "زهرة الربيع",
            "custom": "مخصص"
        },
        "text_animations": {
            "typewriter": "آلة كاتبة",
            "fade_in": "ظهور تدريجي",
            "slide_up": "انزلاق لأعلى",
            "custom": "مخصص"
        },
        "Egypt": "مصر",
        "Cairo": "القاهرة",
        "tomatoes, cucumbers, eggplants": "طماطم، خيار، باذنجان",
        "Yellow spots on leaves": "بقع صفراء على الأوراق",
        "Tomato": "طماطم",
        "From growing gardens to growing mindsets": "من زراعة الحدائق إلى تنمية العقول",
        "Analyze Current Weather": "تحليل الطقس الحالي",
        "Generating recommendations...": "جارٍ إنشاء التوصيات...",
        "Diagnosing...": "جارٍ التشخيص...",
        "You are a plant disease specialist": "أنت متخصص في أمراض النباتات",
        "The affected plant is": "النبات المصاب هو",
        "Visible symptoms are": "الأعراض الظاهرة هي",
        "Please provide": "يرجى تقديم",
        "Likely diagnosis": "التشخيص المحتمل",
        "Possible causes": "الأسباب المحتملة",
        "Recommended treatment": "العلاج الموصى به",
        "Prevention methods": "طرق الوقاية",
        "in a well-organized table": "في جدول منظم جيدًا",
        "You are an agricultural consultant": "أنت مستشار زراعي",
        "I need planting suggestions for": "أحتاج إلى اقتراحات زراعية لـ",
        "in": "في",
        "soil": "تربة",
        "located in": "تقع في",
        "The garden area is": "مساحة الحديقة هي",
        "Current weather": "الطقس الحالي",
        "Crop name": "اسم المحصول",
        "Soil compatibility": "توافق التربة",
        "Weather suitability": "ملاءمة الطقس",
        "Care tips": "نصائح العناية",
        "Here are some web resources about": "إليك بعض الموارد على الإنترنت حول",
        "No relevant info found.": "لم يتم العثور على معلومات ذات صلة.",
        "Search failed:": "فشل البحث:",
        "You are a smart gardening assistant": "أنت مساعد بستنة ذكي",
        "Current weather in": "الطقس الحالي في",
        "Question": "سؤال",
        "Please provide a detailed answer with practical tips": "يرجى تقديم إجابة مفصلة مع نصائح عملية",
        "Error:": "خطأ:",
        "Select Language:": "اختر اللغة:",
        "settings": "الإعدادات",
        "Navigation": "التنقل",
        "watering_schedule": "جدول الري",
        "create_schedule": "إنشاء جدول الري",
        "plant_name": "اسم النبات",
        "water_frequency": "تكرار الري (أيام)",
        "last_watered": "آخر مرة تم الري",
        "next_watering": "الري القادم",
        "add_schedule": "إضافة جدول",
        "no_schedules": "لا توجد جداول ري حتى الآن.",
        "garden_journal": "مذكرات الحديقة",
        "add_journal_entry": "إضافة مدونة جديدة",
        "journal_date": "التاريخ",
        "journal_entry": "المدونة",
        "add_entry": "إضافة مدونة",
        "no_entries": "لا توجد مدونات حتى الآن.",
        "view_journal": "عرض المذكرات",
        "view_schedule": "عرض الجدول",
        "delete": "حذف",
        "edit": "تعديل",
        "save": "حفظ",
        "cancel": "إلغاء",
        "confirm_delete": "هل أنت متأكد من أنك تريد حذف هذا العنصر؟",
        "watering_reminder": "تذكير الري",
        "due_for_watering": "النباتات التالية تحتاج إلى الري اليوم:",
        "no_watering_due": "لا توجد نباتات تحتاج إلى الري اليوم.",
        "journal_prompt": "ماذا لاحظت في حديقتك اليوم؟"
    }
}

def get_text(key):
    """Get translated text based on current language setting"""
    lang = st.session_state.get('language', 'English')
    try:
        return translations[lang].get(key, key)
    except KeyError:
        return key

themes = {
    "nature_green": {
        "primary": "#2e7d32",
        "secondary": "#4caf50",
        "background": "#e8f5e9",
        "text": "#1b5e20",
        "accent": "#81c784"
    },
    "ocean_blue": {
        "primary": "#1976d2",
        "secondary": "#2196f3",
        "background": "#e3f2fd",
        "text": "#0d47a1",
        "accent": "#64b5f6"
    },
    "sunset_orange": {
        "primary": "#e65100",
        "secondary": "#ef6c00",
        "background": "#fff3e0",
        "text": "#bf360c",
        "accent": "#ff9800"
    },
    "forest_green": {
        "primary": "#33691e",
        "secondary": "#689f38",
        "background": "#f1f8e9",
        "text": "#1b5e20",
        "accent": "#8bc34a"
    },
    "spring_blossom": {
        "primary": "#ad1457",
        "secondary": "#d81b60",
        "background": "#fce4ec",
        "text": "#880e4f",
        "accent": "#e91e63"
    },
    "custom": {
        "primary": "#81c784",
        "secondary": "#a5d6a7",
        "background": "#e8f5e9",
        "text": "#1b5e20",
        "accent": "#c8e6c9"
    }
}

text_animations = {
    "typewriter": {
        "css": """
        @keyframes typewriter {
            from { width: 0 }
            to { width: 100% }
        }
        .typewriter {
            overflow: hidden;
            white-space: nowrap;
            animation: typewriter 2s steps(40) 1s 1 normal both;
        }
        """
    },
    "fade_in": {
        "css": """
        @keyframes fadeIn {
            from { opacity: 0 }
            to { opacity: 1 }
        }
        .fadeIn {
            animation: fadeIn 1.5s ease-in;
        }
        """
    },
    "slide_up": {
        "css": """
        @keyframes slideUp {
            from { transform: translateY(20px); opacity: 0 }
            to { transform: translateY(0); opacity: 1 }
        }
        .slideUp {
            animation: slideUp 1s ease-out;
        }
        """
    },
    "custom": {
        "css": """
        @keyframes customAnim {
            0% { opacity: 0; transform: scale(0.8) }
            100% { opacity: 1; transform: scale(1) }
        }
        .customAnim {
            animation: customAnim 1s ease-in-out;
        }
        """
    }
}

def lighten_color(color, percent):
    return color

def darken_color(color, percent):
    return color

def set_theme(theme_name):
    if theme_name not in themes:
        theme_name = 'nature_green'
    theme = themes[theme_name]
    st.markdown(f"""
    <style>
        :root {{
            --primary-color: {theme['primary']};
            --secondary-color: {theme['secondary']};
            --background-color: {theme['background']};
            --text-color: {theme['text']};
            --accent-color: {theme['accent']};
        }}
        .stApp {{
            background-color: {theme['background']};
            color: {theme['text']};
            background-image: radial-gradient({theme['accent']} 1px, transparent 1px);
            background-size: 20px 20px;
            animation: subtlePulse 15s infinite alternate;
        }}
        @keyframes subtlePulse {{
            0% {{ background-color: {theme['background']}; }}
            100% {{ background-color: {lighten_color(theme['background'], 5)}; }}
        }}
        .stButton>button {{
            background-color: {theme['primary']};
            color: white;
            border-radius: 20px;
            transition: all 0.3s;
            border: none;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }}
        .stButton>button:hover {{
            background-color: {theme['secondary']};
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        .stTextInput>div>div>input, 
        .stSelectbox>div>div>select,
        .stNumberInput>div>div>input,
        .stTextArea>div>div>textarea {{
            background-color: white;
            border-radius: 10px;
            border: 1px solid {theme['primary']};
            transition: all 0.3s;
        }}
        .stTextInput>div>div>input:focus, 
        .stSelectbox>div>div>select:focus,
        .stNumberInput>div>div>input:focus,
        .stTextArea>div>div>textarea:focus {{
            border: 2px solid {theme['primary']};
            box-shadow: 0 0 0 2px {theme['accent']};
        }}
        .stTabs [data-baseweb="tab-list"] {{
            gap: 10px;
        }}
        .stTabs [data-baseweb="tab"] {{
            background-color: {theme['accent']};
            border-radius: 10px 10px 0 0 !important;
            transition: all 0.3s;
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {theme['primary']} !important;
            color: white !important;
        }}
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
            color: {theme['text']};
            position: relative;
            display: inline-block;
        }}
        .stMarkdown h1::after, .stMarkdown h2::after {{
            content: '';
            position: absolute;
            width: 100%;
            height: 3px;
            bottom: -5px;
            left: 0;
            background: linear-gradient(90deg, {theme['primary']}, {theme['accent']});
            transform: scaleX(0);
            transform-origin: right;
            transition: transform 0.5s ease;
        }}
        .stMarkdown h1:hover::after, .stMarkdown h2:hover::after {{
            transform: scaleX(1);
            transform-origin: left;
        }}
        .css-1aumxhk {{
            background-color: {theme['background']};
        }}
        .info-button {{
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 1000;
        }}
        .info-button button {{
            padding: 5px 10px;
            font-size: 12px;
            border-radius: 50%;
            width: 30px;
            height: 30px;
        }}
    </style>
    """, unsafe_allow_html=True)

def set_text_animation(animation_name):
    if animation_name not in text_animations:
        animation_name = 'typewriter'
    anim = text_animations[animation_name]
    st.markdown(f"""
    <style>
    {anim['css']}
    .animated-text {{
        {''.join(anim['css'].split('}')[-2].split('{')[1:])}
    }}
    </style>
    """, unsafe_allow_html=True)

def get_weather_data(city):
    if not city:
        st.warning(get_text("Please enter a city name"))
        return None
    url = f'http://api.weatherstack.com/current?access_key=c1330aec5aad5b56cf63fca9fb0ffef7&query={city}'
    try:
        response = req.get(url)
        if response.status_code == 200:
            data = response.json()
            return None if 'error' in data else data
        return None
    except Exception as e:
        st.error(f"{get_text('weather_error')}: {str(e)}")
        return None

def display_weather_info(city):
    data = st.session_state.weather_data
    if data and 'current' in data:
        current = data['current']
        st.subheader(f"{get_text('weather_data')} {city}")
        cols = st.columns(2)
        with cols[0]:
            st.metric(get_text('temperature'), f"{current['temperature']}°C")
            st.metric(get_text('humidity'), f"{current['humidity']}%")
        with cols[1]:
            st.metric(get_text('wind_speed'), f"{current['wind_speed']} km/h")
            st.metric(get_text('observation_time'), current['observation_time'])
        if current.get('weather_descriptions'):
            st.write(f"{get_text('Weather description')}: {current['weather_descriptions'][0]}")
        return current
    else:
        st.error(get_text("weather_error"))
        return None

def diagnose_plant_disease(plant_type, symptoms):
    if not plant_type or not symptoms:
        st.warning(get_text("Please provide both plant type and symptoms"))
        return None
    prompt = f"""
    {get_text("You are a plant disease specialist")}. 
    {get_text("The affected plant is")}: {plant_type}.
    {get_text("Visible symptoms are")}: {symptoms}.
    {get_text("Please provide")}:
    1. {get_text("Likely diagnosis")}
    2. {get_text("Possible causes")}
    3. {get_text("Recommended treatment")}
    4. {get_text("Prevention methods")}
    {get_text("in a well-organized table")}
    """
    with st.spinner(get_text("Diagnosing...")):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            st.error(f"{get_text('disease_error')}: {str(e)}")
            return None

def generate_crop_analysis(crops, soil, city, country, area, unit):
    weather_info = ""
    if st.session_state.weather_data and 'current' in st.session_state.weather_data:
        wd = st.session_state.weather_data['current']
        weather_info = f"""
        {get_text("Current weather")}:
        - {get_text("Temperature")}: {wd['temperature']}°C
        - {get_text("Humidity")}: {wd['humidity']}%
        - {get_text("Wind speed")}: {wd['wind_speed']} km/h
        """
    prompt = f"""
    {get_text("You are an agricultural consultant")}. 
    {get_text("I need planting suggestions for")}: {crops} 
    {get_text("in")} {soil} {get_text("soil")}, 
    {get_text("located in")} {city}, {country}.
    {get_text("The garden area is")} {area} {unit}.
    {weather_info}
    {get_text("Please provide a summary table with")}:
    1. {get_text("Crop name")}
    2. {get_text("Soil compatibility")}
    3. {get_text("Weather suitability")}
    4. {get_text("Care tips")}
    """
    return prompt.strip()

def search_web(query):
    if not query:
        return get_text("Please enter a search query")
    try:
        search_results = list(search(query, num_results=3, advanced=True))
        if search_results:
            response = f"{get_text('Here are some web resources about')} '{query}':\n\n"
            for i, result in enumerate(search_results, 1):
                response += f"{i}. [{result.title}]({result.url})\n"
            return response
        return get_text("No relevant info found.")
    except Exception as e:
        return f"{get_text('Search failed:')} {str(e)}"

def show_version_info():
    st.session_state.show_info = True

def hide_version_info():
    st.session_state.show_info = False

def toggle_settings():
    st.session_state.show_settings = not st.session_state.show_settings

def add_watering_schedule(plant_name, frequency, last_watered):
    next_watering = last_watered + timedelta(days=frequency)
    schedule = {
        "plant_name": plant_name,
        "frequency": frequency,
        "last_watered": last_watered,
        "next_watering": next_watering
    }
    st.session_state.watering_schedules.append(schedule)

def update_watering_schedule(index, plant_name, frequency, last_watered):
    next_watering = last_watered + timedelta(days=frequency)
    st.session_state.watering_schedules[index] = {
        "plant_name": plant_name,
        "frequency": frequency,
        "last_watered": last_watered,
        "next_watering": next_watering
    }

def delete_watering_schedule(index):
    if 0 <= index < len(st.session_state.watering_schedules):
        st.session_state.watering_schedules.pop(index)

def add_journal_entry(date, entry):
    journal = {
        "date": date,
        "entry": entry
    }
    st.session_state.garden_journals.append(journal)

def update_journal_entry(index, date, entry):
    st.session_state.garden_journals[index] = {
        "date": date,
        "entry": entry
    }

def delete_journal_entry(index):
    if 0 <= index < len(st.session_state.garden_journals):
        st.session_state.garden_journals.pop(index)

def get_watering_reminders():
    today = datetime.now().date()
    due_plants = []
    for schedule in st.session_state.watering_schedules:
        if schedule["next_watering"].date() <= today:
            due_plants.append(schedule["plant_name"])
    return due_plants

def main():
    # Info button at top right
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("ℹ️", key="info_button", help=get_text("version_info"), use_container_width=True):
            show_version_info()
    
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3039/3039013.png", width=100)
        st.title(get_text("Garden Assistant"))
        st.markdown("### " + get_text("Navigation"))
        
        # Settings button
        if st.button("⚙️ " + get_text("settings"), use_container_width=True):
            toggle_settings()
        
        # Settings expander
        if st.session_state.show_settings:
            with st.expander(get_text("settings"), expanded=True):
                st.session_state.language = st.selectbox(
                    get_text("Select Language:"), 
                    ['English', 'العربية'],
                    index=0 if st.session_state.language == 'English' else 1
                )
                st.session_state.theme = st.selectbox(
                    get_text("theme_select"),
                    list(themes.keys()),
                    format_func=lambda x: get_text("themes")[x],
                    index=list(themes.keys()).index(st.session_state.theme)
                )
                st.session_state.text_animation = st.selectbox(
                    get_text("text_animation_select"),
                    list(text_animations.keys()),
                    format_func=lambda x: get_text("text_animations")[x],
                    index=list(text_animations.keys()).index(st.session_state.text_animation)
                )
        
        set_theme(st.session_state.theme)
        set_text_animation(st.session_state.text_animation)
        
        # Watering reminders
        due_plants = get_watering_reminders()
        if due_plants:
            st.warning(f"💧 {get_text('watering_reminder')}")
            for plant in due_plants:
                st.write(f"- {plant}")
        else:
            st.success(f"✅ {get_text('no_watering_due')}")
    
    if st.session_state.show_info:
        with st.container():
            st.markdown(f"### {get_text('app_version')}")
            st.markdown(f"**{get_text('features')}:**")
            for feature in get_text("feature_list"):
                st.markdown(f"- {feature}")
            if st.button(get_text("close")):
                hide_version_info()
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🌱 " + get_text("title"), 
        "🌿 " + get_text("section4"),
        "💬 " + get_text("section5"),
        "💧 " + get_text("section6"),
        "📔 " + get_text("section7")
    ])
    
    with tab1:
        st.markdown(f"""
        <h1 class="animated-text" style="text-align: center; color: var(--text-color);">
        🌿 {get_text("title")} 🌿
        </h1>
        """, unsafe_allow_html=True)
        with st.expander(get_text("section1"), expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                unit = st.selectbox(
                    get_text("unit"), 
                    get_text("units")
                )
            with col2:
                area = st.number_input(
                    get_text("area"), 
                    min_value=1, 
                    value=10,
                    help=get_text("area") + " " + get_text("in square meters")
                )       
        with st.expander(get_text("section2"), expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                country = st.text_input(
                    get_text("country"), 
                    value=get_text("Egypt")
                )
            with col2:
                city = st.text_input(
                    get_text("city"), 
                    value=get_text("Cairo")
                )
            soil = st.selectbox(
                get_text("soil"), 
                get_text("soils")
            )
            if st.button("🔍 " + get_text("Analyze Current Weather")):
                st.session_state.weather_data = get_weather_data(city)
            if st.session_state.weather_data:
                display_weather_info(city)
        with st.expander(get_text("section3"), expanded=True):
            crops = st.text_area(
                get_text("crops"), 
                value=get_text("tomatoes, cucumbers, eggplants"),
                help=get_text("crops") + " " + get_text("(comma separated)")
            )
            if st.button(get_text("analyze")):
                if not crops:
                    st.warning(get_text("Please enter crops to analyze"))
                else:
                    prompt = generate_crop_analysis(crops, soil, city, country, area, unit)
                    with st.spinner(get_text("Generating recommendations...")):
                        try:
                            response = model.generate_content(prompt)
                            st.markdown(response.text)
                        except Exception as e:
                            st.error(f"{get_text('Error:')} {str(e)}")
    
    with tab2:
        st.markdown(f"""
        <h1 class="animated-text" style="color: var(--text-color);">
        🌿 {get_text("disease_title")}
        </h1>
        """, unsafe_allow_html=True)
        with st.form("plant_diagnosis_form"):
            plant_type = st.text_input(
                get_text("plant_type"), 
                value=get_text("Tomato")
            )
            symptoms = st.text_area(
                get_text("plant_symptoms"), 
                value=get_text("Yellow spots on leaves")
            )
            submitted = st.form_submit_button(
                "🔍 " + get_text("diagnose")
            )
            if submitted:
                if not plant_type or not symptoms:
                    st.warning(get_text("Please provide both plant type and symptoms"))
                else:
                    diagnosis = diagnose_plant_disease(plant_type, symptoms)
                    if diagnosis:
                        st.session_state.plant_disease_data = diagnosis
                        st.success(get_text("disease_success"))
                        st.markdown("### " + get_text("treatment"))
                        st.markdown(diagnosis)
        
        if st.session_state.plant_disease_data:
            st.markdown("### " + get_text("Previous Diagnosis"))
            st.markdown(st.session_state.plant_disease_data)
    
    with tab3:
        st.markdown(f"""
        <h1 class="animated-text" style="color: var(--text-color);">
        💬 {get_text("chat_title")}
        </h1>
        """, unsafe_allow_html=True)
        search_web_checkbox = st.checkbox(
            get_text("search_web"),
            help=get_text("search_web") + " " + get_text("to get web results")
        )
        user_input = st.text_input(
            get_text("chat_placeholder"), 
            key="chat_input",
            placeholder=get_text("chat_placeholder"),
            value=st.session_state.edit_text if st.session_state.editing_index is not None else ""
        )
        if user_input:
            if st.session_state.editing_index is not None:
                if st.session_state.editing_index < len(st.session_state['past']):
                    st.session_state['past'][st.session_state.editing_index] = user_input
                st.session_state.editing_index = None
                st.session_state.edit_text = ""
                st.experimental_rerun()
            else:
                st.session_state.past.append(user_input)
                if search_web_checkbox:
                    response = search_web(user_input)
                    st.session_state.generated.append(response)
                else:
                    weather_context = ""
                    city = st.session_state.get('city', get_text("Cairo"))
                    if st.session_state.weather_data and 'current' in st.session_state.weather_data:
                        wd = st.session_state.weather_data['current']
                        weather_context = f"""
                        {get_text("Current weather in")} {city}:
                        - {get_text("Temperature")}: {wd['temperature']}°C
                        - {get_text("Humidity")}: {wd['humidity']}%
                        - {get_text("Wind speed")}: {wd['wind_speed']} km/h
                        """
                    prompt = f"""
                    {get_text("You are a smart gardening assistant")}.
                    {weather_context}
                    {get_text("Question")}: {user_input}
                    {get_text("Please provide a detailed answer with practical tips")}
                    """
                    with st.spinner(get_text("chat_response")):
                        try:
                            response = model.generate_content(prompt)
                            st.session_state.generated.append(response.text)
                        except Exception as e:
                            st.session_state.generated.append(
                                f"{get_text('Error:')} {str(e)}"
                            )
        if st.session_state['generated']:
            for i in range(len(st.session_state['generated']) - 1, -1, -1):
                message(st.session_state["generated"][i], key=str(i))
                if i < len(st.session_state['past']):
                    col1, col2 = st.columns([8, 1])
                    with col1:
                        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                    with col2:
                        if st.button("✏️", key=f"edit_{i}"):
                            st.session_state.editing_index = i
                            st.session_state.edit_text = st.session_state['past'][i]
                            st.experimental_rerun()
    
    with tab4:
        st.markdown(f"""
        <h1 class="animated-text" style="color: var(--text-color);">
        💧 {get_text("watering_schedule")}
        </h1>
        """, unsafe_allow_html=True)
        
        with st.expander(get_text("create_schedule"), expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                plant_name = st.text_input(get_text("plant_name"))
            with col2:
                frequency = st.number_input(get_text("water_frequency"), min_value=1, value=7)
            
            last_watered = st.date_input(get_text("last_watered"), datetime.now())
            
            if st.button(get_text("add_schedule")):
                if plant_name:
                    add_watering_schedule(plant_name, frequency, last_watered)
                    st.success(f"Added watering schedule for {plant_name}")
                else:
                    st.warning("Please enter a plant name")
        
        st.markdown("### " + get_text("view_schedule"))
        if not st.session_state.watering_schedules:
            st.info(get_text("no_schedules"))
        else:
            for i, schedule in enumerate(st.session_state.watering_schedules):
                col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
                with col1:
                    st.write(f"**{schedule['plant_name']}**")
                with col2:
                    st.write(f"{get_text('water_frequency')}: {schedule['frequency']} days")
                with col3:
                    st.write(f"{get_text('last_watered')}: {schedule['last_watered'].strftime('%Y-%m-%d')}")
                with col4:
                    st.write(f"{get_text('next_watering')}: {schedule['next_watering'].strftime('%Y-%m-%d')}")
                
                col_edit, col_del = st.columns(2)
                with col_edit:
                    if st.button(f"✏️ {get_text('edit')}", key=f"edit_schedule_{i}"):
                        st.session_state.editing_schedule_index = i
                with col_del:
                    if st.button(f"🗑️ {get_text('delete')}", key=f"delete_schedule_{i}"):
                        delete_watering_schedule(i)
                        st.experimental_rerun()
            
            if 'editing_schedule_index' in st.session_state:
                i = st.session_state.editing_schedule_index
                schedule = st.session_state.watering_schedules[i]
                
                st.markdown("---")
                st.markdown(f"### Editing {schedule['plant_name']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    edit_plant_name = st.text_input(get_text("plant_name"), value=schedule['plant_name'], key=f"edit_plant_{i}")
                with col2:
                    edit_frequency = st.number_input(get_text("water_frequency"), min_value=1, value=schedule['frequency'], key=f"edit_freq_{i}")
                
                edit_last_watered = st.date_input(get_text("last_watered"), value=schedule['last_watered'], key=f"edit_last_{i}")
                
                col_save, col_cancel = st.columns(2)
                with col_save:
                    if st.button(get_text("save"), key=f"save_schedule_{i}"):
                        update_watering_schedule(i, edit_plant_name, edit_frequency, edit_last_watered)
                        del st.session_state.editing_schedule_index
                        st.experimental_rerun()
                with col_cancel:
                    if st.button(get_text("cancel"), key=f"cancel_schedule_{i}"):
                        del st.session_state.editing_schedule_index
                        st.experimental_rerun()
    
    with tab5:
        st.markdown(f"""
        <h1 class="animated-text" style="color: var(--text-color);">
        📔 {get_text("garden_journal")}
        </h1>
        """, unsafe_allow_html=True)
        
        with st.expander(get_text("add_journal_entry"), expanded=True):
            journal_date = st.date_input(get_text("journal_date"), datetime.now())
            journal_entry = st.text_area(get_text("journal_entry"), placeholder=get_text("journal_prompt"), height=150)
            
            if st.button(get_text("add_entry")):
                if journal_entry:
                    add_journal_entry(journal_date, journal_entry)
                    st.success("Journal entry added!")
                else:
                    st.warning("Please write something in your journal")
        
        st.markdown("### " + get_text("view_journal"))
        if not st.session_state.garden_journals:
            st.info(get_text("no_entries"))
        else:
            # Sort journals by date (newest first)
            sorted_journals = sorted(st.session_state.garden_journals, key=lambda x: x['date'], reverse=True)
            
            for i, journal in enumerate(sorted_journals):
                st.markdown(f"**{journal['date'].strftime('%Y-%m-%d')}**")
                st.write(journal['entry'])
                
                col_edit, col_del = st.columns(2)
                with col_edit:
                    if st.button(f"✏️ {get_text('edit')}", key=f"edit_journal_{i}"):
                        st.session_state.editing_journal_index = i
                with col_del:
                    if st.button(f"🗑️ {get_text('delete')}", key=f"delete_journal_{i}"):
                        # Find the original index of this journal
                        original_index = st.session_state.garden_journals.index(journal)
                        delete_journal_entry(original_index)
                        st.experimental_rerun()
                
                st.markdown("---")
            
            if 'editing_journal_index' in st.session_state:
                i = st.session_state.editing_journal_index
                journal = sorted_journals[i]
                
                # Find the original index of this journal
                original_index = st.session_state.garden_journals.index(journal)
                
                st.markdown("---")
                st.markdown(f"### Editing journal entry from {journal['date'].strftime('%Y-%m-%d')}")
                
                edit_journal_date = st.date_input(get_text("journal_date"), value=journal['date'], key=f"edit_date_{i}")
                edit_journal_entry = st.text_area(get_text("journal_entry"), value=journal['entry'], height=150, key=f"edit_entry_{i}")
                
                col_save, col_cancel = st.columns(2)
                with col_save:
                    if st.button(get_text("save"), key=f"save_journal_{i}"):
                        update_journal_entry(original_index, edit_journal_date, edit_journal_entry)
                        del st.session_state.editing_journal_index
                        st.experimental_rerun()
                with col_cancel:
                    if st.button(get_text("cancel"), key=f"cancel_journal_{i}"):
                        del st.session_state.editing_journal_index
                        st.experimental_rerun()
    
    st.markdown(f"""
    <div style="text-align: center; margin-top: 50px; padding: 20px; position: relative;">
        <div id="growing-plant" style="width: 50px; height: 50px; margin: 0 auto; 
                    background-image: url('https://cdn-icons-png.flaticon.com/512/3039/3039013.png');
                    background-size: contain;
                    background-repeat: no-repeat;
                    animation: grow 5s infinite alternate;">
        </div>
        <p class="animated-text" style="color: var(--text-color); margin-top: 10px;">
            🌱 {get_text("From growing gardens to growing mindsets")} 🌱
        </p>
    </div>
    <style>
    @keyframes grow {{
        0% {{ transform: scale(0.8); opacity: 0.7; }}
        100% {{ transform: scale(1.1); opacity: 1; }}
    }}
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        @media (max-width: 768px) {
            .stApp {
                padding: 10px;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    if st.session_state.language == 'العربية':
        st.markdown("""
        <style>
            .stApp [dir='ltr'] {text-align: right;}
            .stTextInput>div>div>input, .stSelectbox>div>div>select,
            .stNumberInput>div>div>input {text-align: right;}
        </style>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
