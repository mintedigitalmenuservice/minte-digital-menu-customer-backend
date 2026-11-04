

# Minte Digital Menu Backend. Web
# Run: uvicorn main:app --reload  
# Run: uvicorn customer_menu:app --host 0.0.0.0 --port 8000 

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import os


app = FastAPI()

# ========== CORS ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== SESSION STORAGE ==========
user_sessions = {}

# ========== PATHS ==========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CUSTOMER_JSON_PATH = os.path.join(BASE_DIR, "minte_hotel_digital_menu.json")

# ========== LOAD JSON ==========
def load_json():
    try:
        with open(
            CUSTOMER_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(
            "Error: minte_hotel_digital_menu.json not found")
        return {}
    except json.JSONDecodeError:
        print(
            "Error: JSON file is corrupted")
        return {}

# ========== SERVE IMAGES ==========
app.mount(
    "/images", 
    StaticFiles(directory=os.path.join(BASE_DIR, "images")),
    name="images")

app.mount(
    "/hotel_image",
    StaticFiles(directory=os.path.join(BASE_DIR, "hotel_image")),
    name="hotel_image" )

# ========== API ROUTES ==========
@app.get("/api/languages")
def get_languages():
    bot_data = load_json()
    language = bot_data.get("language_menu", {})
    buttons = []

    for key, value in language.items():
        name = value.get("starts",{}).get("name", key)
        buttons.append({"key": key, "name": name})
    return {
        "buttons": buttons
    }

class LanguageRequest(BaseModel):
    lang_key: str

@app.post("/api/select_language")
def select_language(data: LanguageRequest):
    
    lang_key = data.lang_key

    # Load JSON
    bot_data = load_json()

    # ========== GET LANGUAGE DATA ==========
    if lang_key in bot_data.get("language_menu",{}):
        lang_data = bot_data["language_menu"][lang_key]
    else:
        language_menu = bot_data.get("language_menu", {})

        if not language_menu:
            return {
                "error": "No languages found"
            }

        first_key = list(language_menu.keys())[0]
        lang_data = language_menu[first_key]

    # ========== HOTEL NAME ==========
    hotel_name = "Minte Hotel"

    # ========== ABOUT ==========
    about_text = lang_data.get("about", "Welcome to Minte hotel!")

    # ========== CONTACT ==========
    contact_text = lang_data.get("contact", "📍 Location: Dilla, Ethiopia\n📞 Phone: 0951388278")

    # ==================================================
    # FOOD
    # ==================================================
    food_items = []
    if ("food" in lang_data and "product" in lang_data["food"]):
        for key, item in lang_data["food"]["product"].items():
            if (key != "types" and isinstance(item, dict)):
                price_label = item.get("lang_price", "Price")
                
                currency = item.get("currenc", "$")

                price_value = item.get("price",0)

                food_items.append({
                    "id": f"food_{key}",
                    "name": item.get("name", key),
                    "price": (
                        f"{price_label}: "
                        f"{price_value}"
                        f"{currency}"
                        ),
                    "description": item.get(
                        "description",
                        ""
                    ),
                    "image": item.get(
                        "image",
                        ""
                    ),
                    "category": "food",
                    "visible": item.get("visible", True)
                })

    # ==================================================
    # DRINKS
    # ==================================================
    drink_items = []

    if ("drink" in lang_data and "product" in lang_data["drink"]):
        for key, item in lang_data["drink"]["product"].items():
            if (key != "types" and isinstance(item, dict)):
                price_label = item.get("lang_price", "Price")

                currency = item.get("currenc", "$")

                price_value = item.get("price",0)

                drink_items.append({
                    "id": f"drink_{key}",
                    "name": item.get("name", key),
                    "price": (
                        f"{price_label}: "
                        f"{price_value}"
                        f"{currency}"
                    ),
                    "description": item.get("description", ""),
                    "image": item.get("image", ""),
                    "category": "drinks",
                    "visible": item.get("visible", True)
                })


    # ==================================================
    # ROOMS
    # ==================================================
    room_items = []
    
    if ("room" in lang_data and "room_list" in lang_data["room"]):

        for key, item in lang_data["room"]["room_list"].items():
            if (key != "types" and isinstance(item, dict)):

                price_label = item.get("lang_price", "Price")

                currency = item.get("currenc", "$")

                price_value = item.get("price",0)

                room_items.append({
                    "id": f"room_{key}",
                    "name": item.get("name", key),
                    "price": (
                        f"{price_label}: "
                        f"{price_value}"
                        f"{currency}"
                    ),
                    "description": item.get("description", ""),
                    "image": item.get("image", ""),
                    "category": "rooms",
                    "visible": item.get("visible", True)
                })


    # ==================================================
    # VIP ROOMS
    # ==================================================
    vip_room_items = []

    if ("vip_room" in lang_data and "room_list" in lang_data["vip_room"]):
        for key, item in lang_data["vip_room"]["room_list"].items():
            if (key != "types" and isinstance(item, dict)):
                price_label = item.get("lang_price", "Price")

                currency = item.get("currenc", "$")

                price_value = item.get("price",0)

                vip_room_items.append({
                    "id": f"vip_room_{key}",
                    "name": item.get("name", key),
                    "price": (
                        f"{price_label}: "
                        f"{price_value}"
                        f"{currency}"
                    ),
                    "description": item.get("description", ""),
                    "image": item.get("image", ""),
                    "category": "vip_rooms",
                    "visible": item.get("visible", True)
                })

    # ========== LOG ==========
    print(
        f"✅ Loaded: "
        f"{len(food_items)} food, "
        f"{len(drink_items)} drinks, "
        f"{len(room_items)} rooms, "
        f"{len(vip_room_items)} VIP rooms "
        f"for {lang_key}"
    )

    # ========== RESPONSE ==========
    return {
        "hotel_name": hotel_name,
        "about_text": about_text,
        "contact_text": contact_text,
        "food_items": food_items,
        "drink_items": drink_items,
        "room_items": room_items,
        "vip_room_items": vip_room_items,
    }
    
