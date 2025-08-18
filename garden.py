import streamlit as st
from streamlit.components.v1 import html
import google.generativeai as genai
from streamlit_chat import message
from googlesearch import search
import requests as req
import random
import json
from datetime import datetime, timedelta
from PIL import Image
import io
import base64
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from geopy.geocoders import Nominatim
import pytz
from timezonefinder import TimezoneFinder
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import calendar
from typing import Optional, Dict, List, Tuple, Union, Any
import av
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

# Constants
APP_VERSION = "4.1"
MAX_CHAT_HISTORY = 50
MAX_PLANT_TYPES = 100
MAX_SOIL_TYPES = 20
MAX_CROPS = 50
MAX_WEATHER_RETRIES = 3
WEATHER_CACHE_TIME = 3600 
DEFAULT_THEME = 'nature_green'
DEFAULT_LANGUAGE = 'English'
DEFAULT_ANIMATION = 'typewriter'

def initialize_session_state():
    session_defaults = {
        'generated': [],
        'past': [],
        'weather_data': None,
        'weather_last_fetched': 0,
        'plant_disease_data': None,
        'theme': DEFAULT_THEME,
        'language': DEFAULT_LANGUAGE,
        'animation_style': 'floating_leaves',
        'text_animation': DEFAULT_ANIMATION,
        'editing_index': None,
        'edit_text': "",
        'show_info': False,
        'user_preferences': {},
        'saved_gardens': [],
        'current_garden': None,
        'plant_library': [],
        'crop_rotation_plans': [],
        'watering_schedule': {},
        'garden_layouts': {},
        'planting_calendar': {},
        'garden_journal': [],
        'notifications': [],
        'data_consent': False,
        'user_location': None,
        'garden_images': [],
        'plant_progress': {},
        'harvest_records': [],
        'pest_alerts': [],
        'soil_test_results': {},
        'garden_budget': {},
        'tool_inventory': [],
        'compost_data': {},
        'irrigation_system': {},
        'garden_goals': [],
        'plant_companions': {},
        'garden_tasks': [],
        'weather_alerts': [],
        'plant_wishlist': [],
        'garden_stats': {},
        'ai_model': 'gemini-pro',
        'api_usage': {},
        'error_log': [],
        'ui_settings': {
            'font_size': 'medium',
            'contrast': 'normal',
            'animation_speed': 'normal'
        },
        'camera_mode': False,
        'video_finished': False
    }
    
    for key, value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# ======================
# TRANSLATION SYSTEM
# ======================
class TranslationSystem:
    def __init__(self):
        self.translations = {
            'English': self._load_english_translations(),
            'Arabic': self._load_arabic_translations()
        }
    
    def _load_english_translations(self) -> Dict[str, Any]:
        return {
            "title": "Smart Garden Planning System",
            "section1": "Garden Dimensions",
            "section2": "Soil and Weather Information",
            "section3": "Planting Suggestions",
            "section4": "Plant Disease Diagnosis",
            "section5": "Smart Garden Assistant",
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
                "Plant progress tracking",
                "Garden journal",
                "Crop rotation planner",
                "Watering schedule",
                "Pest management",
                "Harvest records",
                "Soil health monitoring"
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
            "garden_journal": "Garden Journal",
            "add_journal_entry": "Add Journal Entry",
            "journal_date": "Date",
            "journal_entry": "Entry",
            "journal_photos": "Photos",
            "save_journal": "Save Entry",
            "view_journal": "View Journal",
            "watering_schedule": "Watering Schedule",
            "plant_name": "Plant Name",
            "watering_frequency": "Watering Frequency",
            "last_watered": "Last Watered",
            "next_watering": "Next Watering",
            "add_schedule": "Add to Schedule",
            "update_schedule": "Update Schedule",
            "plant_progress": "Plant Progress",
            "progress_date": "Date Recorded",
            "progress_notes": "Progress Notes",
            "growth_stage": "Growth Stage",
            "height": "Height (cm)",
            "health_status": "Health Status",
            "record_progress": "Record Progress",
            "view_progress": "View Progress History",
            "harvest_records": "Harvest Records",
            "harvest_date": "Harvest Date",
            "harvest_amount": "Amount Harvested",
            "harvest_quality": "Quality",
            "harvest_notes": "Notes",
            "record_harvest": "Record Harvest",
            "view_harvests": "View Harvest History",
            "pest_alerts": "Pest Alerts",
            "pest_name": "Pest Name",
            "pest_severity": "Severity",
            "pest_date": "Date Observed",
            "pest_actions": "Actions Taken",
            "add_pest_alert": "Add Pest Alert",
            "view_pest_alerts": "View Pest Alerts",
            "soil_tests": "Soil Tests",
            "test_date": "Test Date",
            "ph_level": "pH Level",
            "nutrients": "Nutrient Levels",
            "soil_notes": "Notes",
            "record_soil_test": "Record Soil Test",
            "view_soil_tests": "View Soil Test History",
            "garden_tasks": "Garden Tasks",
            "task_name": "Task Name",
            "task_due": "Due Date",
            "task_priority": "Priority",
            "task_status": "Status",
            "add_task": "Add Task",
            "view_tasks": "View All Tasks",
            "complete_task": "Mark Complete",
            "data_consent": "Data Collection Consent",
            "consent_text": "I agree to share anonymous usage data to improve the app",
            "give_consent": "Give Consent",
            "revoke_consent": "Revoke Consent",
            "notifications": "Notifications",
            "view_notifications": "View Notifications",
            "clear_notifications": "Clear All",
            "settings": "Settings",
            "save_settings": "Save Settings",
            "reset_settings": "Reset to Defaults",
            "help": "Help",
            "feedback": "Send Feedback",
            "privacy": "Privacy Policy",
            "terms": "Terms of Service",
            "contact": "Contact Support",
            "import_data": "Import Data",
            "export_data": "Export Data",
            "backup": "Backup & Restore",
            "plant_library": "Plant Library",
            "add_plant": "Add Plant to Library",
            "plant_details": "Plant Details",
            "scientific_name": "Scientific Name",
            "family": "Family",
            "sun_requirements": "Sun Requirements",
            "water_requirements": "Water Needs",
            "planting_season": "Planting Season",
            "days_to_harvest": "Days to Harvest",
            "spacing": "Spacing (cm)",
            "depth": "Planting Depth (cm)",
            "save_plant": "Save Plant",
            "view_library": "View Plant Library",
            "crop_rotation": "Crop Rotation",
            "rotation_year": "Year",
            "rotation_season": "Season",
            "rotation_bed": "Garden Bed",
            "rotation_crop": "Planted Crop",
            "add_rotation": "Add Rotation Plan",
            "view_rotation": "View Rotation History",
            "garden_layout": "Garden Layout",
            "layout_name": "Layout Name",
            "layout_plants": "Plants in Layout",
            "layout_design": "Design Notes",
            "save_layout": "Save Layout",
            "view_layouts": "View Saved Layouts",
            "planting_calendar": "Planting Calendar",
            "calendar_month": "Month",
            "calendar_tasks": "Monthly Tasks",
            "calendar_planting": "Planting Dates",
            "calendar_harvest": "Harvest Dates",
            "save_calendar": "Save Calendar",
            "view_calendar": "View Full Calendar",
            "garden_budget": "Garden Budget",
            "budget_item": "Item",
            "budget_cost": "Cost",
            "budget_category": "Category",
            "budget_date": "Purchase Date",
            "add_expense": "Add Expense",
            "view_budget": "View Budget Report",
            "tool_inventory": "Tool Inventory",
            "tool_name": "Tool Name",
            "tool_condition": "Condition",
            "tool_last_maintenance": "Last Maintenance",
            "add_tool": "Add Tool",
            "view_tools": "View All Tools",
            "compost": "Compost Tracker",
            "compost_date": "Date Started",
            "compost_materials": "Materials",
            "compost_turn_dates": "Turn Dates",
            "compost_ready": "Ready Date",
            "add_compost": "Add Compost Batch",
            "view_compost": "View Compost History",
            "irrigation": "Irrigation System",
            "irrigation_type": "System Type",
            "irrigation_schedule": "Watering Schedule",
            "irrigation_zones": "Zones",
            "irrigation_notes": "Maintenance Notes",
            "save_irrigation": "Save Irrigation Setup",
            "view_irrigation": "View Irrigation Details",
            "garden_goals": "Garden Goals",
            "goal_name": "Goal Name",
            "goal_target": "Target Date",
            "goal_status": "Progress",
            "goal_notes": "Notes",
            "add_goal": "Add Goal",
            "view_goals": "View All Goals",
            "plant_companions": "Companion Plants",
            "main_plant": "Main Plant",
            "companion_plants": "Good Companions",
            "antagonist_plants": "Plants to Avoid",
            "add_companions": "Add Companion Info",
            "view_companions": "View Companion Guide",
            "garden_stats": "Garden Statistics",
            "stats_plants": "Total Plants",
            "stats_varieties": "Plant Varieties",
            "stats_harvest": "Total Harvest",
            "stats_success": "Success Rate",
            "view_stats": "View Detailed Stats",
            "ai_settings": "AI Settings",
            "ai_model": "AI Model",
            "ai_temperature": "Creativity Level",
            "ai_max_tokens": "Response Length",
            "save_ai_settings": "Save AI Preferences",
            "api_usage": "API Usage",
            "api_calls": "Total Calls",
            "api_errors": "Errors",
            "api_last_used": "Last Used",
            "view_api_usage": "View API Statistics",
            "error_log": "Error Log",
            "error_time": "Time",
            "error_message": "Error Message",
            "error_details": "Details",
            "view_errors": "View Error Log",
            "clear_errors": "Clear Error Log",
            "ui_settings": "UI Settings",
            "font_size": "Font Size",
            "contrast": "Contrast",
            "animation_speed": "Animation Speed",
            "save_ui_settings": "Save UI Preferences",
            "plant_wishlist": "Plant Wishlist",
            "wishlist_plant": "Plant Name",
            "wishlist_priority": "Priority",
            "wishlist_notes": "Notes",
            "add_to_wishlist": "Add to Wishlist",
            "view_wishlist": "View Wishlist",
            "weather_alerts": "Weather Alerts",
            "alert_type": "Alert Type",
            "alert_date": "Date",
            "alert_severity": "Severity",
            "alert_actions": "Recommended Actions",
            "add_alert": "Add Weather Alert",
            "view_alerts": "View Weather Alerts",
            "garden_info": "Garden Information Guide",
            "download_info": "Download Guide",
            "take_photo": "Take Photo",
            "camera_mode": "Camera Mode",
            "capture_photo": "Capture Photo",
            "system_info": "System Information",
            "app_intro": "Welcome to Smart Garden Assistant",
            "smart_garden_planner": "Smart Garden Planner",
            "plant_doctor": "Plant Doctor",
            "ai_assistant": "AI Assistant",
            "journal": "Garden Journal",
            "watering": "Watering Schedule",
            "in square meters": "in square meters",
            "(comma separated)": "(comma separated)",
            "No journal entries yet. Add your first entry above!": "No journal entries yet. Add your first entry above!",
            "No plants need watering today!": "No plants need watering today!",
            "Garden Assistant": "Garden Assistant",
            "Upcoming Waterings": "Upcoming Waterings",
            "days overdue": "days overdue",
            "Write your garden observations here...": "Write your garden observations here...",
            "Upload": "Upload",
            "Weather:": "Weather:",
            "It's hot! Consider:": "It's hot! Consider:",
            "Watering plants early morning or late evening": "Watering plants early morning or late evening",
            "Providing shade for sensitive plants": "Providing shade for sensitive plants",
            "Mulching to retain soil moisture": "Mulching to retain soil moisture",
            "It's cold! Consider:": "It's cold! Consider:",
            "Protecting sensitive plants with covers": "Protecting sensitive plants with covers",
            "Moving potted plants indoors": "Moving potted plants indoors",
            "Delaying planting of warm-weather crops": "Delaying planting of warm-weather crops",
            "High humidity! Watch for:": "High humidity! Watch for:",
            "Fungal diseases (increase air circulation)": "Fungal diseases (increase air circulation)",
            "Mold growth (avoid overwatering)": "Mold growth (avoid overwatering)",
            "Windy conditions! Consider:": "Windy conditions! Consider:",
            "Staking tall plants": "Staking tall plants",
            "Protecting young seedlings": "Protecting young seedlings",
            "Securing garden structures": "Securing garden structures"
        }
    
    def _load_arabic_translations(self) -> Dict[str, Any]: 
        return {
            "title": "نظام تخطيط الحديقة الذكية",
            "section1": "أبعاد الحديقة",
            "section2": "معلومات التربة والطقس",
            "section3": "اقتراحات الزراعة",
            "section4": "تشخيص أمراض النباتات",
            "section5": "مساعد الحديقة الذكي",
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
            "treatment": "العلاج الموصى به:",
            "disease_title": "تشخيص أمراض النباتات",
            "chat_title": "مساعد البستنة الذكي",
            "chat_placeholder": "اطرح سؤالك عن البستنة...",
            "search_web": "البحث على الويب",
            "chat_response": "رد المساعد:",
            "weather_data": "بيانات الطقس لـ",
            "observation_time": "وقت الملاحظة:",
            "temperature": "درجة الحرارة:",
            "wind_speed": "سرعة الرياح:",
            "humidity": "الرطوبة:",
            "weather_recommendation": "بناءً على بيانات الطقس في مدينتك، أوصي بما يلي:",
            "weather_error": "خطأ في جلب بيانات الطقس",
            "disease_error": "خطأ في التشخيص",
            "disease_success": "تم التشخيص بنجاح",
            "theme_select": "اختر السمة:",
            "animation_select": "اختر نمط الرسوم المتحركة:",
            "text_animation_select": "اختر حركة النص:",
            "version_info": "معلومات النسخة",
            "app_version": f"مساعد الحديقة الذكي v{APP_VERSION}",
            "features": "الميزات",
            "feature_list": [
                "نظام تخطيط الحديقة الذكية",
                "تشخيص أمراض النباتات",
                "مساعد البستنة بالذكاء الاصطناعي",
                "تكامل مع بيانات الطقس",
                "دعم متعدد اللغات",
                "سمات قابلة للتخصيص",
                "سجل محادثات قابل للتعديل",
                "تتبع تقدم النباتات",
                "يوميات الحديقة",
                "مخطط تناوب المحاصيل",
                "جدول الري",
                "إدارة الآفات",
                "سجلات الحصاد",
                "مراقبة صحة التربة"
            ],
            "close": "إغلاق",
            "themes": {
                "nature_green": "الطبيعة الخضراء",
                "ocean_blue": "المحيط الأزرق",
                "sunset_orange": "غروب الشمس البرتقالي",
                "forest_green": "الغابة الخضراء",
                "spring_blossom": "زهور الربيع",
                "custom": "مخصص"
            },
            "text_animations": {
                "typewriter": "آلة كاتبة",
                "fade_in": "تدرج الظهور",
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
            "in a well-organized table": "في جدول منظم",
            "You are an agricultural consultant": "أنت مستشار زراعي",
            "I need planting suggestions for": "أحتاج إلى اقتراحات زراعة لـ",
            "in": "في",
            "soil": "تربة",
            "located in": "تقع في",
            "The garden area is": "مساحة الحديقة هي",
            "Current weather": "الطقس الحالي",
            "Crop name": "اسم المحصول",
            "Soil compatibility": "توافق التربة",
            "Weather suitability": "ملاءمة الطقس",
            "Care tips": "نصائح العناية",
            "Here are some web resources about": "إليك بعض الموارد على الويب عن",
            "No relevant info found.": "لم يتم العثور على معلومات ذات صلة.",
            "Search failed:": "فشل البحث:",
            "You are a smart gardening assistant": "أنت مساعد بستنة ذكي",
            "Current weather in": "الطقس الحالي في",
            "Question": "سؤال",
            "Please provide a detailed answer with practical tips": "يرجى تقديم إجابة مفصلة مع نصائح عملية",
            "Error:": "خطأ:",
            "Select Language:": "اختر اللغة:",
            "garden_journal": "يوميات الحديقة",
            "add_journal_entry": "إضافة مدونة يومية",
            "journal_date": "التاريخ",
            "journal_entry": "المدونة",
            "journal_photos": "الصور",
            "save_journal": "حفظ المدونة",
            "view_journal": "عرض اليوميات",
            "watering_schedule": "جدول الري",
            "plant_name": "اسم النبات",
            "watering_frequency": "تكرار الري",
            "last_watered": "آخر ري",
            "next_watering": "الري التالي",
            "add_schedule": "إضافة إلى الجدول",
            "update_schedule": "تحديث الجدول",
            "plant_progress": "تقدم النبات",
            "progress_date": "تاريخ التسجيل",
            "progress_notes": "ملاحظات التقدم",
            "growth_stage": "مرحلة النمو",
            "height": "الارتفاع (سم)",
            "health_status": "حالة الصحة",
            "record_progress": "تسجيل التقدم",
            "view_progress": "عرض سجل التقدم",
            "harvest_records": "سجلات الحصاد",
            "harvest_date": "تاريخ الحصاد",
            "harvest_amount": "كمية الحصاد",
            "harvest_quality": "الجودة",
            "harvest_notes": "ملاحظات",
            "record_harvest": "تسجيل الحصاد",
            "view_harvests": "عرض سجل الحصاد",
            "pest_alerts": "تنبيهات الآفات",
            "pest_name": "اسم الآفة",
            "pest_severity": "الشدة",
            "pest_date": "تاريخ الملاحظة",
            "pest_actions": "الإجراءات المتخذة",
            "add_pest_alert": "إضافة تنبيه آفة",
            "view_pest_alerts": "عرض تنبيهات الآفات",
            "soil_tests": "اختبارات التربة",
            "test_date": "تاريخ الاختبار",
            "ph_level": "مستوى الأس الهيدروجيني",
            "nutrients": "مستويات المغذيات",
            "soil_notes": "ملاحظات",
            "record_soil_test": "تسجيل اختبار التربة",
            "view_soil_tests": "عرض سجل اختبارات التربة",
            "garden_tasks": "مهام الحديقة",
            "task_name": "اسم المهمة",
            "task_due": "تاريخ الاستحقاق",
            "task_priority": "الأولوية",
            "task_status": "الحالة",
            "add_task": "إضافة مهمة",
            "view_tasks": "عرض جميع المهام",
            "complete_task": "تمييز كمكتمل",
            "data_consent": "موافقة جمع البيانات",
            "consent_text": "أوافق على مشاركة بيانات الاستخدام المجهولة لتحسين التطبيق",
            "give_consent": "منح الموافقة",
            "revoke_consent": "سحب الموافقة",
            "notifications": "الإشعارات",
            "view_notifications": "عرض الإشعارات",
            "clear_notifications": "مسح الكل",
            "settings": "الإعدادات",
            "save_settings": "حفظ الإعدادات",
            "reset_settings": "إعادة الضبط إلى الافتراضي",
            "help": "مساعدة",
            "feedback": "إرسال ملاحظات",
            "privacy": "سياسة الخصوصية",
            "terms": "شروط الخدمة",
            "contact": "اتصل بالدعم",
            "import_data": "استيراد البيانات",
            "export_data": "تصدير البيانات",
            "backup": "النسخ الاحتياطي والاستعادة",
            "plant_library": "مكتبة النباتات",
            "add_plant": "إضافة نبات إلى المكتبة",
            "plant_details": "تفاصيل النبات",
            "scientific_name": "الاسم العلمي",
            "family": "العائلة",
            "sun_requirements": "متطلبات الشمس",
            "water_requirements": "احتياجات الماء",
            "planting_season": "موسم الزراعة",
            "days_to_harvest": "أيام حتى الحصاد",
            "spacing": "المسافة بين النباتات (سم)",
            "depth": "عمق الزراعة (سم)",
            "save_plant": "حفظ النبات",
            "view_library": "عرض مكتبة النباتات",
            "crop_rotation": "تناوب المحاصيل",
            "rotation_year": "السنة",
            "rotation_season": "الموسم",
            "rotation_bed": "حوض الحديقة",
            "rotation_crop": "المحصول المزروع",
            "add_rotation": "إضافة خطة تناوب",
            "view_rotation": "عرض سجل التناوب",
            "garden_layout": "تخطيط الحديقة",
            "layout_name": "اسم التخطيط",
            "layout_plants": "النباتات في التخطيط",
            "layout_design": "ملاحظات التصميم",
            "save_layout": "حفظ التخطيط",
            "view_layouts": "عرض التخطيطات المحفوظة",
            "planting_calendar": "تقويم الزراعة",
            "calendar_month": "الشهر",
            "calendar_tasks": "مهام الشهر",
            "calendar_planting": "تواريخ الزراعة",
            "calendar_harvest": "تواريخ الحصاد",
            "save_calendar": "حفظ التقويم",
            "view_calendar": "عرض التقويم الكامل",
            "garden_budget": "ميزانية الحديقة",
            "budget_item": "البند",
            "budget_cost": "التكلفة",
            "budget_category": "الفئة",
            "budget_date": "تاريخ الشراء",
            "add_expense": "إضافة مصروف",
            "view_budget": "عرض تقرير الميزانية",
            "tool_inventory": "جرد الأدوات",
            "tool_name": "اسم الأداة",
            "tool_condition": "الحالة",
            "tool_last_maintenance": "آخر صيانة",
            "add_tool": "إضافة أداة",
            "view_tools": "عرض جميع الأدوات",
            "compost": "تتبع السماد",
            "compost_date": "تاريخ البدء",
            "compost_materials": "المواد",
            "compost_turn_dates": "تواريخ التقليب",
            "compost_ready": "تاريخ الجاهزية",
            "add_compost": "إضافة دفعة سماد",
            "view_compost": "عرض سجل السماد",
            "irrigation": "نظام الري",
            "irrigation_type": "نوع النظام",
            "irrigation_schedule": "جدول الري",
            "irrigation_zones": "المناطق",
            "irrigation_notes": "ملاحظات الصيانة",
            "save_irrigation": "حفظ إعدادات الري",
            "view_irrigation": "عرض تفاصيل الري",
            "garden_goals": "أهداف الحديقة",
            "goal_name": "اسم الهدف",
            "goal_target": "تاريخ الهدف",
            "goal_status": "التقدم",
            "goal_notes": "ملاحظات",
            "add_goal": "إضافة هدف",
            "view_goals": "عرض جميع الأهداف",
            "plant_companions": "نباتات مصاحبة",
            "main_plant": "النبات الرئيسي",
            "companion_plants": "نباتات مصاحبة جيدة",
            "antagonist_plants": "نباتات يجب تجنبها",
            "add_companions": "إضافة معلومات النباتات المصاحبة",
            "view_companions": "عرض دليل النباتات المصاحبة",
            "garden_stats": "إحصائيات الحديقة",
            "stats_plants": "إجمالي النباتات",
            "stats_varieties": "أصناف النباتات",
            "stats_harvest": "إجمالي الحصاد",
            "stats_success": "معدل النجاح",
            "view_stats": "عرض الإحصائيات التفصيلية",
            "ai_settings": "إعدادات الذكاء الاصطناعي",
            "ai_model": "نموذج الذكاء الاصطناعي",
            "ai_temperature": "مستوى الإبداع",
            "ai_max_tokens": "طول الاستجابة",
            "save_ai_settings": "حفظ تفضيلات الذكاء الاصطناعي",
            "api_usage": "استخدام API",
            "api_calls": "إجمالي الطلبات",
            "api_errors": "أخطاء",
            "api_last_used": "آخر استخدام",
            "view_api_usage": "عرض إحصائيات API",
            "error_log": "سجل الأخطاء",
            "error_time": "الوقت",
            "error_message": "رسالة الخطأ",
            "error_details": "التفاصيل",
            "view_errors": "عرض سجل الأخطاء",
            "clear_errors": "مسح سجل الأخطاء",
            "ui_settings": "إعدادات واجهة المستخدم",
            "font_size": "حجم الخط",
            "contrast": "التباين",
            "animation_speed": "سرعة الرسوم المتحركة",
            "save_ui_settings": "حفظ تفضيلات واجهة المستخدم",
            "plant_wishlist": "قائمة رغبات النباتات",
            "wishlist_plant": "اسم النبات",
            "wishlist_priority": "الأولوية",
            "wishlist_notes": "ملاحظات",
            "add_to_wishlist": "إضافة إلى قائمة الرغبات",
            "view_wishlist": "عرض قائمة الرغبات",
            "weather_alerts": "تنبيهات الطقس",
            "alert_type": "نوع التنبيه",
            "alert_date": "التاريخ",
            "alert_severity": "الشدة",
            "alert_actions": "الإجراءات الموصى بها",
            "add_alert": "إضافة تنبيه طقس",
            "view_alerts": "عرض تنبيهات الطقس",
            "garden_info": "دليل معلومات الحديقة",
            "download_info": "تحميل الدليل",
            "take_photo": "التقاط صورة",
            "camera_mode": "وضع الكاميرا",
            "capture_photo": "التقاط صورة",
            "system_info": "معلومات النظام",
            "app_intro": "مرحبًا بكم في مساعد الحديقة الذكي",
            "smart_garden_planner": "مخطط الحديقة الذكي",
            "plant_doctor": "طبيب النباتات",
            "ai_assistant": "المساعد الذكي",
            "journal": "يوميات الحديقة",
            "watering": "جدول الري",
            "in square meters": "بالمتر المربع",
            "(comma separated)": "(مفصولة بفواصل)",
            "No journal entries yet. Add your first entry above!": "لا توجد مدونات يومية حتى الآن. أضف مدونتك الأولى أعلاه!",
            "No plants need watering today!": "لا توجد نباتات تحتاج للري اليوم!",
            "Garden Assistant": "مساعد الحديقة",
            "Upcoming Waterings": "الري القادم",
            "days overdue": "أيام متأخرة",
            "Write your garden observations here...": "اكتب ملاحظات حديقتك هنا...",
            "Upload": "رفع",
            "Weather:": "الطقس:",
            "It's hot! Consider:": "الطقس حار! ضع في اعتبارك:",
            "Watering plants early morning or late evening": "ري النباتات في الصباح الباكر أو في وقت متأخر من المساء",
            "Providing shade for sensitive plants": "توفير الظل للنباتات الحساسة",
            "Mulching to retain soil moisture": "التغطية للاحتفاظ برطوبة التربة",
            "It's cold! Consider:": "الطقس بارد! ضع في اعتبارك:",
            "Protecting sensitive plants with covers": "حماية النباتات الحساسة بالأغطية",
            "Moving potted plants indoors": "نقل النباتات المزروعة في أصص إلى الداخل",
            "Delaying planting of warm-weather crops": "تأخير زراعة محاصيل الطقس الدافئ",
            "High humidity! Watch for:": "الرطوبة العالية! راقب:",
            "Fungal diseases (increase air circulation)": "أمراض فطرية (زيادة دوران الهواء)",
            "Mold growth (avoid overwatering)": "نمو العفن (تجنب الإفراط في الري)",
            "Windy conditions! Consider:": "ظروف رياح! ضع في اعتبارك:",
            "Staking tall plants": "تثبيت النباتات الطويلة",
            "Protecting young seedlings": "حماية الشتلات الصغيرة",
            "Securing garden structures": "تأمين هياكل الحديقة"
        }
    
    def get_text(self, key: str) -> str:
        lang = st.session_state.get('language', DEFAULT_LANGUAGE)
        try:
            return self.translations[lang].get(key, key)
        except KeyError:
            return key

translator = TranslationSystem()

class ThemeSystem:
    def __init__(self):
        self.themes = {
            "nature_green": {
                "primary": "#2e7d32",
                "secondary": "#4caf50",
                "background": "#e8f5e9",
                "text": "#1b5e20",
                "accent": "#81c784",
                "success": "#388e3c",
                "warning": "#f57c00",
                "error": "#d32f2f",
                "info": "#1976d2"
            },
            "ocean_blue": {
                "primary": "#1976d2",
                "secondary": "#2196f3",
                "background": "#e3f2fd",
                "text": "#0d47a1",
                "accent": "#64b5f6",
                "success": "#0288d1",
                "warning": "#fbc02d",
                "error": "#d32f2f",
                "info": "#0097a7"
            },
            "sunset_orange": {
                "primary": "#e65100",
                "secondary": "#ef6c00",
                "background": "#fff3e0",
                "text": "#bf360c",
                "accent": "#ff9800",
                "success": "#e65100",
                "warning": "#ff6d00",
                "error": "#dd2c00",
                "info": "#ff6d00"
            },
            "forest_green": {
                "primary": "#1b5e20",
                "secondary": "#2e7d32",
                "background": "#e8f5e9",
                "text": "#004d40",
                "accent": "#4caf50",
                "success": "#2e7d32",
                "warning": "#827717",
                "error": "#c62828",
                "info": "#00695c"
            },
            "spring_blossom": {
                "primary": "#880e4f",
                "secondary": "#ad1457",
                "background": "#fce4ec",
                "text": "#4a148c",
                "accent": "#ec407a",
                "success": "#ad1457",
                "warning": "#ff6f00",
                "error": "#c2185b",
                "info": "#7b1fa2"
            },
            "custom": self._get_custom_theme()
        }
    
    def _get_custom_theme(self) -> Dict[str, str]:
        if 'custom_theme' not in st.session_state:
            st.session_state.custom_theme = {
                "primary": "#6a1b9a",
                "secondary": "#9c27b0",
                "background": "#f3e5f5",
                "text": "#4a148c",
                "accent": "#ab47bc",
                "success": "#7b1fa2",
                "warning": "#ff8f00",
                "error": "#c2185b",
                "info": "#7e57c2"
            }
        return st.session_state.custom_theme
    
    def set_theme(self, theme_name: str) -> None:
        if theme_name not in self.themes:
            theme_name = DEFAULT_THEME
        
        theme = self.themes[theme_name]
        
        st.markdown(f"""
        <style>
            :root {{
                --primary-color: {theme['primary']};
                --secondary-color: {theme['secondary']};
                --background-color: {theme['background']};
                --text-color: {theme['text']};
                --accent-color: {theme['accent']};
                --success-color: {theme['success']};
                --warning-color: {theme['warning']};
                --error-color: {theme['error']};
                --info-color: {theme['info']};
            }}
            .stApp {{
                background-color: var(--background-color);
                color: var(--text-color);
            }}
            h1, h2, h3, h4, h5, h6 {{
                color: var(--primary-color);
            }}
            .stButton>button {{
                background-color: var(--primary-color);
                color: white;
                border-radius: 8px;
                border: none;
                padding: 8px 16px;
            }}
            .stButton>button:hover {{
                background-color: var(--secondary-color);
                color: white;
            }}
            .stTextInput>div>div>input {{
                border: 1px solid var(--accent-color);
                border-radius: 4px;
            }}
            .stSelectbox>div>div {{
                border: 1px solid var(--accent-color);
                border-radius: 4px;
            }}
            .css-1d391kg {{
                background-color: var(--background-color);
                border-right: 1px solid var(--accent-color);
            }}
            .stExpander {{
                border: 1px solid var(--accent-color);
                border-radius: 4px;
            }}
            .stAlert {{
                border-left: 4px solid var(--accent-color);
                background-color: rgba(255, 255, 255, 0.8);
            }}
            .stProgress > div > div > div {{
                background-color: var(--primary-color);
            }}
            .animated-text {{
                color: var(--text-color);
                font-weight: bold;
            }}
            .custom-card {{
                border: 1px solid var(--accent-color);
                border-radius: 8px;
                padding: 16px;
                margin-bottom: 16px;
                background-color: rgba(255, 255, 255, 0.8);
            }}
            .custom-tab {{
                padding: 8px 16px;
                border-radius: 4px;
                background-color: var(--secondary-color);
                color: white;
                margin-right: 8px;
            }}
            .custom-success {{
                color: var(--success-color);
                font-weight: bold;
            }}
            .custom-warning {{
                color: var(--warning-color);
                font-weight: bold;
            }}
            .custom-error {{
                color: var(--error-color);
                font-weight: bold;
            }}
            .custom-info {{
                color: var(--info-color);
                font-weight: bold;
            }}
            .stTabs [data-baseweb="tab-list"] {{
                gap: 8px;
            }}
            .stTabs [data-baseweb="tab"] {{
                background-color: var(--background-color);
                border: 1px solid var(--accent-color);
                border-radius: 8px 8px 0px 0px;
                padding: 8px 16px;
            }}
            .stTabs [aria-selected="true"] {{
                background-color: var(--primary-color);
                color: white;
            }}
        </style>
        """, unsafe_allow_html=True)
        
        st.session_state.theme = theme_name

theme_manager = ThemeSystem()

class AnimationSystem:
    def __init__(self):
        self.animations = {
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
                    from { opacity: 0; }
                    to { opacity: 1; }
                }
                .fade-in {
                    animation: fadeIn 1.5s ease-in;
                }
                """
            },
            "slide_up": {
                "css": """
                @keyframes slideUp {
                    from { transform: translateY(20px); opacity: 0; }
                    to { transform: translateY(0); opacity: 1; }
                }
                .slide-up {
                    animation: slideUp 1s ease-out;
                }
                """
            }
        }
    
    def set_animation(self, animation_name: str) -> None:
        if animation_name not in self.animations:
            animation_name = DEFAULT_ANIMATION
        
        anim = self.animations[animation_name]
        
        st.markdown(f"""
        <style>
        {anim['css']}
        .animated-text {{
            {''.join(anim['css'].split('}')[-2].split('{')[1:])}
        }}
        </style>
        """, unsafe_allow_html=True)
        
        st.session_state.text_animation = animation_name

animation_manager = AnimationSystem()

class WeatherService:
    def __init__(self):
        self.api_key = "c1330aec5aad5b56cf63fca9fb0ffef7"
        self.base_url = "http://api.weatherstack.com/current"
        self.cache = {}
    
    def get_weather(self, city: str) -> Optional[Dict[str, Any]]:
        if not city:
            st.warning(translator.get_text("Please enter a city name"))
            return None
        
        cached_data = self._check_cache(city)
        if cached_data:
            return cached_data
        
        url = f"{self.base_url}?access_key={self.api_key}&query={city}"
        
        for attempt in range(MAX_WEATHER_RETRIES):
            try:
                response = req.get(url)
                if response.status_code == 200:
                    data = response.json()
                    if 'error' in data:
                        st.error(f"{translator.get_text('weather_error')}: {data['error']['info']}")
                        return None
                    
                    self._cache_weather(city, data)
                    return data
            except Exception as e:
                if attempt == MAX_WEATHER_RETRIES - 1:
                    st.error(f"{translator.get_text('weather_error')}: {str(e)}")
                    return None
                time.sleep(1) 
        
        return None
    
    def _check_cache(self, city: str) -> Optional[Dict[str, Any]]:
        if city in self.cache:
            cached_time, data = self.cache[city]
            if time.time() - cached_time < WEATHER_CACHE_TIME:
                return data
        return None
    
    def _cache_weather(self, city: str, data: Dict[str, Any]) -> None:
        self.cache[city] = (time.time(), data)

weather_service = WeatherService()

class AIService:
    def __init__(self):
        try:
            genai.configure(api_key="AIzaSyA5RMHXOoVasqXObWwTZwusBqG1y9Cihtk")
            self.model = genai.GenerativeModel('gemini-pro')
            self.retries = 3
            self.timeout = 30
        except Exception as e:
            st.error(f"Failed to initialize AI model: {str(e)}")
            self.model = None
    
    def generate_response(self, prompt: str) -> Optional[str]:
        if not self.model:
            return translator.get_text("AI service is not available")
        
        for attempt in range(self.retries):
            try:
                response = self.model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": 0.7,
                        "max_output_tokens": 2000,
                    }
                )
                return response.text
            except Exception as e:
                if attempt == self.retries - 1:
                    return f"{translator.get_text('Error:')} {str(e)}"
                time.sleep(1)
        
        return translator.get_text("Failed to get AI response after retries")

ai_service = AIService()

class GardenPlanner:
    def __init__(self):
        self.plant_db = self._load_plant_database()
        self.soil_types = translator.get_text("soils")
        self.weather_impacts = {
            'hot': ['cucumber', 'melon', 'pepper'],
            'cold': ['kale', 'spinach', 'broccoli'],
            'wet': ['rice', 'cranberry', 'taro'],
            'dry': ['cactus', 'succulent', 'lavender']
        }
    
    def _load_plant_database(self) -> Dict[str, Any]:
        return {
            'tomato': {
                'scientific_name': 'Solanum lycopersicum',
                'family': 'Solanaceae',
                'sun': 'full',
                'water': 'moderate',
                'soil': ['loamy', 'sandy'],
                'companions': ['basil', 'marigold'],
                'incompatible': ['cabbage', 'fennel']
            },
            'cucumber': {
                'scientific_name': 'Cucumis sativus',
                'family': 'Cucurbitaceae',
                'sun': 'full',
                'water': 'high',
                'soil': ['loamy', 'silty'],
                'companions': ['beans', 'peas'],
                'incompatible': ['potato', 'sage']
            },
            'eggplant': {
                'scientific_name': 'Solanum melongena',
                'family': 'Solanaceae',
                'sun': 'full',
                'water': 'moderate',
                'soil': ['loamy', 'sandy'],
                'companions': ['beans', 'spinach'],
                'incompatible': ['fennel', 'corn']
            }
        }
    
    def analyze_crops(self, crops: str, soil: str, city: str, 
                     country: str, area: float, unit: str) -> str:
        weather_context = ""
        if st.session_state.weather_data and 'current' in st.session_state.weather_data:
            wd = st.session_state.weather_data['current']
            weather_context = f"""
            {translator.get_text("Current weather")}:
            - {translator.get_text("Temperature")}: {wd['temperature']}°C
            - {translator.get_text("Humidity")}: {wd['humidity']}%
            - {translator.get_text("Wind speed")}: {wd['wind_speed']} km/h
            """
        
        prompt = f"""
        {translator.get_text("You are an agricultural consultant")}. 
        {translator.get_text("I need planting suggestions for")}: {crops} 
        {translator.get_text("in")} {soil} {translator.get_text("soil")}, 
        {translator.get_text("located in")} {city}, {country}.
        {translator.get_text("The garden area is")} {area} {unit}.
        {weather_context}
        {translator.get_text("Please provide a detailed analysis including")}:
        1. {translator.get_text("Crop name")}
        2. {translator.get_text("Soil compatibility")} (1-5 rating)
        3. {translator.get_text("Weather suitability")} (1-5 rating)
        4. {translator.get_text("Care tips")}
        5. Optimal planting dates
        6. Expected yield per square meter
        7. Common pests and prevention
        8. Harvesting timeline
        9. Storage recommendations
        10. Companion planting suggestions
        Present in a comprehensive, well-organized markdown table with 
        separate sections for each crop.
        """
        
        return ai_service.generate_response(prompt)

garden_planner = GardenPlanner()

class PlantDoctor:
    def diagnose(self, plant_type: str, symptoms: str) -> Optional[str]:
        if not plant_type or not symptoms:
            st.warning(translator.get_text("Please provide both plant type and symptoms"))
            return None
        
        prompt = f"""
        {translator.get_text("You are a plant disease specialist")}. 
        {translator.get_text("The affected plant is")}: {plant_type}.
        {translator.get_text("Visible symptoms are")}: {symptoms}.
        {translator.get_text("Please provide")}:
        1. {translator.get_text("Likely diagnosis")} (most probable 3 diseases)
        2. {translator.get_text("Possible causes")} (environmental, pests, etc.)
        3. {translator.get_text("Recommended treatment")} (organic and chemical options)
        4. {translator.get_text("Prevention methods")} (for future)
        5. Quarantine recommendations
        6. Photos of similar cases for comparison
        7. Expected recovery timeline
        8. When to seek professional help
        {translator.get_text("in a well-organized table")} with severity indicators.
        Include emojis for visual cues (🌱 for mild, 🚨 for severe).
        """
        
        return ai_service.generate_response(prompt)

plant_doctor = PlantDoctor()

class WebSearch:
    def search(self, query: str, num_results: int = 3) -> str:
        if not query:
            return translator.get_text("Please enter a search query")
        
        try:
            search_results = list(search(query, num_results=num_results, advanced=True))
            if search_results:
                response = f"{translator.get_text('Here are some web resources about')} '{query}':\n\n"
                for i, result in enumerate(search_results, 1):
                    response += f"{i}. [{result.title}]({result.url})\n"
                return response
            return translator.get_text("No relevant info found.")
        except Exception as e:
            return f"{translator.get_text('Search failed:')} {str(e)}"

web_searcher = WebSearch()

class GardenJournal:
    def __init__(self):
        self.captured_image = None
    
    def add_entry(self, date: str, entry: str, photos: List[Any]) -> None:
        if not date or not entry:
            st.warning(translator.get_text("Please provide both date and entry text"))
            return
        
        new_entry = {
            "id": len(st.session_state.garden_journal) + 1,
            "date": date,
            "entry": entry,
            "photos": photos,
            "created_at": datetime.now().isoformat()
        }
        st.session_state.garden_journal.append(new_entry)
        st.success(translator.get_text("Journal entry saved successfully"))
    
    def get_entries(self) -> List[Dict[str, Any]]:
        return sorted(
            st.session_state.garden_journal,
            key=lambda x: x["date"],
            reverse=True
        )
    
    def capture_image(self):
        """Capture image from camera"""
        def video_frame_callback(frame):
            img = frame.to_ndarray(format="bgr24")
            self.captured_image = img
            return frame
        
        webrtc_ctx = webrtc_streamer(
            key="camera",
            video_frame_callback=video_frame_callback,
            media_stream_constraints={"video": True, "audio": False},
            rtc_configuration=RTCConfiguration(
                {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
            ))
        
        if st.button(translator.get_text("capture_photo")) and self.captured_image is not None:
            return Image.fromarray(self.captured_image)
        return None

garden_journal = GardenJournal()

class WateringScheduler:
    def add_schedule(self, plant_name: str, frequency: str, last_watered: str) -> None:
        if not all([plant_name, frequency, last_watered]):
            st.warning(translator.get_text("Please fill all fields"))
            return
        
        last_watered_date = datetime.strptime(last_watered, "%Y-%m-%d")
        next_watering = self._calculate_next_watering(last_watered_date, frequency)
        
        schedule = {
            "plant_name": plant_name,
            "frequency": frequency,
            "last_watered": last_watered,
            "next_watering": next_watering.strftime("%Y-%m-%d")
        }
        st.session_state.watering_schedule[plant_name] = schedule
        st.success(translator.get_text("Watering schedule updated"))
    
    def _calculate_next_watering(self, last_date: datetime, frequency: str) -> datetime:
        freq_map = {
            "daily": 1,
            "every 2 days": 2,
            "weekly": 7,
            "bi-weekly": 14,
            "monthly": 30
        }
        days = freq_map.get(frequency.lower(), 7)
        return last_date + timedelta(days=days)
    
    def get_due_waterings(self) -> List[Dict[str, Any]]:
        today = datetime.now().date()
        due = []
        for plant, schedule in st.session_state.watering_schedule.items():
            next_date = datetime.strptime(schedule["next_watering"], "%Y-%m-%d").date()
            if next_date <= today:
                due.append({
                    "plant": plant,
                    "last_watered": schedule["last_watered"],
                    "next_watering": schedule["next_watering"],
                    "days_overdue": (today - next_date).days
                })
        return sorted(due, key=lambda x: x["days_overdue"], reverse=True)

watering_scheduler = WateringScheduler()

def show_garden_planner():
    st.markdown(f"""
    <h1 class="animated-text" style="text-align: center; color: var(--text-color);">
    🌿 {translator.get_text("smart_garden_planner")} 🌿
    </h1>
    """, unsafe_allow_html=True)
    
    with st.expander(translator.get_text("section1"), expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            unit = st.selectbox(
                translator.get_text("unit"), 
                translator.get_text("units")
            )
        with col2:
            area = st.number_input(
                translator.get_text("area"), 
                min_value=1, 
                value=10,
                help=translator.get_text("area") + " " + translator.get_text("in square meters")
            )
        
        col1, col2 = st.columns(2)
        with col1:
            country = st.text_input(
                translator.get_text("country"), 
                value=translator.get_text("Egypt")
            )
        with col2:
            city = st.text_input(
                translator.get_text("city"), 
                value=translator.get_text("Cairo")
            )
        
        soil = st.selectbox(
            translator.get_text("soil"), 
            translator.get_text("soils")
        )
        
        if st.button("🔍 " + translator.get_text("Analyze Current Weather")):
            st.session_state.weather_data = weather_service.get_weather(city)
        
        if st.session_state.weather_data:
            display_weather_info(city)
    
    with st.expander(translator.get_text("section3"), expanded=True):
        crops = st.text_area(
            translator.get_text("crops"), 
            value=translator.get_text("tomatoes, cucumbers, eggplants"),
            help=translator.get_text("crops") + " " + translator.get_text("(comma separated)")
        )
        
        if st.button(translator.get_text("analyze")):
            if not crops:
                st.warning(translator.get_text("Please enter crops to analyze"))
            else:
                with st.spinner(translator.get_text("Generating recommendations...")):
                    analysis = garden_planner.analyze_crops(
                        crops, soil, city, country, area, unit
                    )
                    st.markdown(analysis)

def show_plant_doctor():
    st.markdown(f"""
    <h1 class="animated-text" style="color: var(--text-color);">
    🌿 {translator.get_text("plant_doctor")}
    </h1>
    """, unsafe_allow_html=True)
    
    with st.form("plant_diagnosis_form"):
        plant_type = st.text_input(
            translator.get_text("plant_type"), 
            value=translator.get_text("Tomato")
        )
        symptoms = st.text_area(
            translator.get_text("plant_symptoms"), 
            value=translator.get_text("Yellow spots on leaves")
        )
        submitted = st.form_submit_button("🔍 " + translator.get_text("diagnose"))
        
        if submitted:
            if not plant_type or not symptoms:
                st.warning(translator.get_text("Please provide both plant type and symptoms"))
            else:
                diagnosis = plant_doctor.diagnose(plant_type, symptoms)
                if diagnosis:
                    st.session_state.plant_disease_data = diagnosis
                    st.success(translator.get_text("disease_success"))
                    st.markdown("### " + translator.get_text("treatment"))
                    st.markdown(diagnosis)
    
    if st.session_state.plant_disease_data:
        st.markdown("### " + translator.get_text("Previous Diagnosis"))
        st.markdown(st.session_state.plant_disease_data)

def show_garden_assistant():
    st.markdown(f"""
    <h1 class="animated-text" style="color: var(--text-color);">
    💬 {translator.get_text("ai_assistant")}
    </h1>
    """, unsafe_allow_html=True)
    
    search_web_checkbox = st.checkbox(
        translator.get_text("search_web"),
        help=translator.get_text("search_web") + " " + translator.get_text("to get web results")
    )
    
    user_input = st.text_input(
        translator.get_text("chat_placeholder"), 
        key="chat_input",
        placeholder=translator.get_text("chat_placeholder"),
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
                response = web_searcher.search(user_input)
                st.session_state.generated.append(response)
            else:
                weather_context = ""
                city = st.session_state.get('city', translator.get_text("Cairo"))
                if st.session_state.weather_data and 'current' in st.session_state.weather_data:
                    wd = st.session_state.weather_data['current']
                    weather_context = f"""
                    {translator.get_text("Current weather in")} {city}:
                    - {translator.get_text("Temperature")}: {wd['temperature']}°C
                    - {translator.get_text("Humidity")}: {wd['humidity']}%
                    - {translator.get_text("Wind speed")}: {wd['wind_speed']} km/h
                    """
                
                prompt = f"""
                {translator.get_text("You are a smart gardening assistant")}.
                {weather_context}
                {translator.get_text("Question")}: {user_input}
                {translator.get_text("Please provide a detailed answer with practical tips")}
                """
                
                with st.spinner(translator.get_text("chat_response")):
                    response = ai_service.generate_response(prompt)
                    st.session_state.generated.append(response)
    
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

def show_garden_journal():
    st.markdown(f"""
    <h1 class="animated-text" style="color: var(--text-color);">
    📔 {translator.get_text("journal")}
    </h1>
    """, unsafe_allow_html=True)
    
    with st.expander("➕ " + translator.get_text("add_journal_entry"), expanded=True):
        entry_date = st.date_input(
            translator.get_text("journal_date"),
            value=datetime.now()
        )
        entry_text = st.text_area(
            translator.get_text("journal_entry"),
            height=150,
            placeholder=translator.get_text("Write your garden observations here...")
        )
        
        st.markdown(f"### 📷 {translator.get_text('take_photo')}")
        camera_tab, upload_tab = st.tabs([translator.get_text("camera_mode"), translator.get_text("Upload")])
        uploaded_photos = []
        
        with camera_tab:
            if st.button(translator.get_text("camera_mode")):
                st.session_state.camera_mode = True
            if st.session_state.camera_mode:
                captured_image = garden_journal.capture_image()
                if captured_image:
                    uploaded_photos.append(captured_image)
                    st.session_state.camera_mode = False
                    st.rerun()
        
        with upload_tab:
            uploaded_files = st.file_uploader(
                translator.get_text("journal_photos"),
                type=['jpg', 'jpeg', 'png'],
                accept_multiple_files=True
            )
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    uploaded_photos.append(Image.open(uploaded_file))
        
        if st.button(translator.get_text("save_journal")):
            garden_journal.add_entry(
                entry_date.strftime("%Y-%m-%d"),
                entry_text,
                uploaded_photos
            )
    
    st.markdown("## " + translator.get_text("view_journal"))
    entries = garden_journal.get_entries()
    if not entries:
        st.info(translator.get_text("No journal entries yet. Add your first entry above!"))
    else:
        for entry in entries:
            with st.container():
                st.markdown(f"### {entry['date']}")
                st.write(entry['entry'])
                if entry['photos']:
                    cols = st.columns(min(3, len(entry['photos'])))
                    for i, photo in enumerate(entry['photos']):
                        with cols[i % 3]:
                            st.image(photo, use_column_width=True)
                st.markdown("---")

def show_watering_scheduler():
    st.markdown(f"""
    <h1 class="animated-text" style="color: var(--text-color);">
    💧 {translator.get_text("watering")}
    </h1>
    """, unsafe_allow_html=True)
    
    with st.expander("➕ " + translator.get_text("add_schedule"), expanded=True):
        plant_name = st.text_input(
            translator.get_text("plant_name"),
            placeholder="Tomato Plant #1"
        )
        frequency = st.selectbox(
            translator.get_text("watering_frequency"),
            options=["daily", "every 2 days", "weekly", "bi-weekly", "monthly"]
        )
        last_watered = st.date_input(
            translator.get_text("last_watered"),
            value=datetime.now()
        )
        
        if st.button(translator.get_text("add_schedule")):
            watering_scheduler.add_schedule(
                plant_name,
                frequency,
                last_watered.strftime("%Y-%m-%d")
            )
    
    st.markdown("## " + translator.get_text("Upcoming Waterings"))
    due_waterings = watering_scheduler.get_due_waterings()
    
    if not due_waterings:
        st.success(translator.get_text("No plants need watering today!"))
    else:
        for watering in due_waterings:
            with st.container():
                cols = st.columns([3, 2, 2, 1])
                with cols[0]:
                    st.markdown(f"**{watering['plant']}**")
                with cols[1]:
                    st.markdown(f"Last: {watering['last_watered']}")
                with cols[2]:
                    st.markdown(f"Next: {watering['next_watering']}")
                with cols[3]:
                    if st.button("✅", key=f"watered_{watering['plant']}"):
                        watering_scheduler.add_schedule(
                            watering["plant"],
                            watering["frequency"],
                            datetime.now().strftime("%Y-%m-%d")
                        )
                        st.experimental_rerun()
                
                if watering['days_overdue'] > 0:
                    st.warning(f"{watering['days_overdue']} {translator.get_text('days overdue')}")
                st.markdown("---")

def display_weather_info(city: str) -> None:
    data = st.session_state.weather_data
    if data and 'current' in data:
        current = data['current']
        st.subheader(f"{translator.get_text('weather_data')} {city}")
        
        cols = st.columns(2)
        with cols[0]:
            st.metric(translator.get_text('temperature'), f"{current['temperature']}°C")
            st.metric(translator.get_text('humidity'), f"{current['humidity']}%")
        with cols[1]:
            st.metric(translator.get_text('wind_speed'), f"{current['wind_speed']} km/h")
            st.metric(translator.get_text('observation_time'), current['observation_time'])
        
        if current.get('weather_descriptions'):
            st.write(f"{translator.get_text('Weather:')} {current['weather_descriptions'][0]}")
        
        with st.expander(translator.get_text("weather_recommendation")):
            if current['temperature'] > 30:
                st.write(f"🌞 {translator.get_text('It\'s hot! Consider:')}")
                st.write(f"- {translator.get_text('Watering plants early morning or late evening')}")
                st.write(f"- {translator.get_text('Providing shade for sensitive plants')}")
                st.write(f"- {translator.get_text('Mulching to retain soil moisture')}")
            elif current['temperature'] < 10:
                st.write(f"❄️ {translator.get_text('It\'s cold! Consider:')}")
                st.write(f"- {translator.get_text('Protecting sensitive plants with covers')}")
                st.write(f"- {translator.get_text('Moving potted plants indoors')}")
                st.write(f"- {translator.get_text('Delaying planting of warm-weather crops')}")
            
            if current['humidity'] > 80:
                st.write(f"💧 {translator.get_text('High humidity! Watch for:')}")
                st.write(f"- {translator.get_text('Fungal diseases (increase air circulation)')}")
                st.write(f"- {translator.get_text('Mold growth (avoid overwatering)')}")
            
            if current['wind_speed'] > 20:
                st.write(f"💨 {translator.get_text('Windy conditions! Consider:')}")
                st.write(f"- {translator.get_text('Staking tall plants')}")
                st.write(f"- {translator.get_text('Protecting young seedlings')}")
                st.write(f"- {translator.get_text('Securing garden structures')}")

def show_system_info():
    st.markdown("### " + translator.get_text("system_info"))
    st.markdown(f"""
    **{translator.get_text('app_version')}**  
    **Features:**
    - Smart garden planning system
    - Plant disease diagnosis
    - AI-powered gardening assistant
    - Weather integration
    - Multi-language support
    - Customizable themes
    """)
    
    st.markdown("### " + translator.get_text("contact"))
    st.write("For support, please contact: support@gardenai.com")

def main():
    initialize_session_state()
    
    # Apply theme and animation settings
    theme_manager.set_theme(st.session_state.theme)
    animation_manager.set_animation(st.session_state.text_animation)
    
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3039/3039013.png", width=100)
        st.title(translator.get_text("Garden Assistant"))
        st.markdown("### " + translator.get_text("Navigation"))
        
        with st.expander("⚙️ " + translator.get_text("settings")):
            st.session_state.language = st.selectbox(
                translator.get_text("Select Language:"), 
                ['English', 'Arabic'],
                index=['English', 'Arabic'].index(st.session_state.language)
            )
            
            st.session_state.theme = st.selectbox(
                translator.get_text("theme_select"),
                list(theme_manager.themes.keys()),
                format_func=lambda x: translator.get_text("themes")[x],
                index=list(theme_manager.themes.keys()).index(st.session_state.theme)
            )
            
            st.session_state.text_animation = st.selectbox(
                translator.get_text("text_animation_select"),
                ["typewriter", "fade_in", "slide_up"],
                index=["typewriter", "fade_in", "slide_up"].index(st.session_state.text_animation)
            )
            
            if st.button(translator.get_text("system_info")):
                show_system_info()
            
            if st.button(translator.get_text("save_settings")):
                st.success(translator.get_text("Settings saved"))
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🌱 " + translator.get_text("smart_garden_planner"),
        "🌿 " + translator.get_text("plant_doctor"),
        "💬 " + translator.get_text("ai_assistant"),
        "📔 " + translator.get_text("journal"),
        "💧 " + translator.get_text("watering")
    ])
    
    with tab1:
        show_garden_planner()
    with tab2:
        show_plant_doctor()
    with tab3:
        show_garden_assistant()
    with tab4:
        show_garden_journal()
    with tab5:
        show_watering_scheduler()
    
    st.markdown(f"""
    <div style="text-align: center; margin-top: 50px; padding: 20px;">
        <p class="animated-text" style="color: var(--text-color);">
            🌱 {translator.get_text("From growing gardens to growing mindsets")} 🌱
        </p>
        <small>{translator.get_text("app_version")}</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
