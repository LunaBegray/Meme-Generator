from flask import Flask, send_file, jsonify, request
from PIL import Image, ImageDraw, ImageFont
import os
import random
import requests
from io import BytesIO

app = Flask(__name__)

# Paths
TEMPLATES_PATH = "templates"  # Folder for meme templates
FONT_PATH = "arial.ttf"       # Ensure you have this or replace with another available font

# Imgflip API details
IMGFLIP_USERNAME = 'lunashoval'
IMGFLIP_PASSWORD = 'luna5143'
IMGFLIP_URL = 'https://api.imgflip.com/get_memes'

CAPTIONS = [
    "me trying to explain\nwhy I need 8 hours of sleep\nand 3 naps",
    "when you realize\nyou're the main character\nbut also the villain",
    "  slay but in pain  ",
    "no thoughts,\njust vibes",
    "when someone says\n'be yourself,'\nbut you're an introvert",
    "this ain't it,\nbut it'll do",
    "POV: you tried\nto fix your sleep schedule",
    "ratio + L +\ncry about it",
    "me after gaslighting\nmyself into thinking\nI'm fine",
    "sus vibes detected\n💀",
    "touch grass\nbut like gently",
    "when you're\nmid-tier at everything,\nbut that's your charm",
    "gaslight\ngatekeep\ngirlboss",
    "me explaining how\nthe $7 iced coffee\nis a personality trait",
    "brain: stop overthinking\nme: overthinks harder",
    "when the audacity\nof others\noutweighs your will to care",
    "  emotionally unavailable  \nbut make it aesthetic",
    "when someone says\n'slay,' but you're\nalready slaying by existing",
    "POV: you've convinced yourself\nthat tomorrow is 'future you's'\nproblem",
    "cringe?\nI call it\ncharacter development",
    "me after sending\none (1) email:\nI need a 3-day vacation",
    "when you're\n99% sure you have\na 'rare condition'",
    "sleep is for the weak\nbut also for the\nmentally stable",
    "being the funny friend\nbut also unironically\ndepressed",
    "why have boundaries\nwhen you can just\nsuffer silently?",
    "when you’re too old\nfor TikTok\but too young\nfor Facebook",
    "zero productivity,\nbut the vibes\nare immaculate",
    "i woke up like this,\nand honestly,\nI'm going back to bed",
    "being the problem\nbut also the solution\nis my toxic trait",
    "  living in the moment  \nbut only for the plot",
    "when the 'treat yourself'\nmentality turns into\nfinancial ruin",
    "me thinking about\nthe thing I said\n3 years ago",
    "POV: your whole personality\nis based on\ninternet culture",
    "life hack:\njust don't",
    "I didn’t choose\nthis NPC energy,\nit chose me",
    "  adulting is a scam  ",
    "why save money\nwhen you can just\nregret later?",
    "slay,\nbut at what cost?",
    "how it feels to chew\n5Gum\nbut emotionally",
    "every day is leg day\nwhen you run\nfrom your problems",
    "therapy?\nbut make it\ncryptic tweets",
    "POV: you 'forgot'\nto respond for\n3 business days",
    "when you realize\nyou've unlocked\nthe 'boss battle' stage of life",
    "normalize not normalizing\nanything ever again",
    "main character energy\nwith a side of\nexistential dread",
    "existence is cringe,\nbut here we are",
    "when someone says\n'it'll get better,'\nbut it's giving mid",
    "me pretending\nto care:\nOscar-worthy performance",
    "  slay responsibly  ",
    "POV: you're avoiding responsibilities\nby making a playlist\nabout avoiding responsibilities",
    "plot twist:\nthe villain was\ncapitalism all along",
    "you either slay\nor get slayed,\nthere is no in-between",
    "  nothing matters  \nexcept my iced coffee",
    "me when I'm productive\nfor 5 minutes:\n*reward unlocked*",
    "fun fact:\nI don't have\nfun facts",
    "when you send\na risky text\nand immediately regret it",
    "this outfit screams\n'I overthink for sport'",
    "me talking to my\nfuture self:\nwhy are you like this?",
    "when life gives you lemons,\nthrow them at\nan existential crisis",
    "  can I opt out  \nof the plot?",
    "being bad at socializing\nbut somehow\nmaking it your brand",
    "when the Wi-Fi is down,\nand you’re forced\nto confront yourself",
    "POV: you're vibing\nbut also spiraling",
    "  accountability  ?\nI don’t know her",
    "me running away\nfrom my problems\nlike it's cardio",
    "why solve problems\nwhen you can just\nprocrastinate?",
    "when your coping mechanisms\nbecome personality traits",
    "  humble but delusional  ",
    "POV: your playlist is\njust the same 3 songs\non repeat",
    "me: I deserve a treat\nalso me:\n*cries over credit card bill*",
    "if 'fake it till you make it'\nwas a sport,\nI'd have Olympic gold",
    "  emotionally stable  \nbut only during\nGolden Hour",
    "when you're googling\n'symptoms of success'\nbut it's giving broke",
    "everyone says\n'work smarter, not harder,'\nbut I'm doing neither",
    "  chasing dreams  \nand tripping over reality",
    "POV: you're arguing\nwith the microwave\nabout how long\nyour food should cook",
    "me vs. me:\nthe endless saga",
    "life is just\none big side quest",
    "being extra\nbut also lazy:\nthe duality of me",
    "  plot twist:\nthe vibes were off all along  ",
    "when someone says\n'spread positivity,'\nbut you're allergic to optimism",
    "POV: you're at the gym\nbut only for\nthe aesthetic mirrors",
    "  vibes immaculate,\nbank account desolate  ",
    "me googling 'how to adult'\nat 2am",
    "when life hands you lemons,\nbut you're already drowning\nin lemonade",
    "  cringe is dead  \nlong live cringe",
    "POV: you forgot\nto charge your social battery",
    "me sending 'lol'\nlike a cry for help",
    "  touch grass  \nbut also,\ndon't touch me",
    "POV: your only personality trait\nis finding everything\n'so relatable'",
    "  nothing to prove,\nnothing to lose  \nand also,\nno motivation",
    "when your entire aesthetic\nis 'I tried'\nand failed fabulously"
]

# Function to fetch meme templates from Imgflip API
def fetch_random_meme():
    try:
        # Request to get the meme templates from Imgflip API
        response = requests.get(IMGFLIP_URL)
        if response.status_code == 200:
            memes = response.json()['data']['memes']
            random_meme = random.choice(memes)  # Select a random meme template
            meme_url = random_meme['url']      # The URL of the meme image
            # Download the meme image
            image_response = requests.get(meme_url)
            if image_response.status_code == 200:
                return Image.open(BytesIO(image_response.content))
    except Exception as e:
        print(f"Error fetching meme from Imgflip API: {e}")
    return None  # Return None if API fails

# Function to randomly pick a template and add text
def generate_meme():
    # Check for local templates first
    templates = os.listdir(TEMPLATES_PATH) if os.path.exists(TEMPLATES_PATH) else []
    
    if templates:
        # Use a local template if available
        template_name = random.choice(templates)
        template_path = os.path.join(TEMPLATES_PATH, template_name)
        image = Image.open(template_path)
    else:
        # Fallback to Imgflip API if no templates are found locally
        image = fetch_random_meme()
        if image is None:
            raise ValueError("No local templates found, and failed to fetch a meme from the Imgflip API.")

    draw = ImageDraw.Draw(image)

    # Pick a random caption
    caption = random.choice(CAPTIONS)

    # Set font size based on image width
    font_size = int(image.width * 0.05)
    font = ImageFont.truetype(FONT_PATH, font_size)

    # Split caption into lines and calculate vertical placement
    lines = caption.split("\n")
    text_height = sum([(draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1]) for line in lines])
    y = (image.height - text_height) // 2  # Center vertically

    # Draw each line on the image
    for line in lines:
        text_bbox = draw.textbbox((0, 0), line, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        x = (image.width - text_width) // 2  # Center horizontally
        draw.text((x, y), line, fill="white", stroke_fill="black", stroke_width=2, font=font)
        y += text_height + 5  # Add line spacing


    # Save generated meme
    output_path = "generated_meme.jpg"
    image.save(output_path)
    return output_path

@app.route("/")
def index():
    try:
        # Generate a new meme
        meme_path = generate_meme()
        return send_file(meme_path, mimetype="image/jpeg")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Ensure the templates folder exists
    if not os.path.exists(TEMPLATES_PATH):
        os.makedirs(TEMPLATES_PATH)
        print(f"Put meme templates in the '{TEMPLATES_PATH}' folder if available.")

    # Run the Flask app
    app.run(debug=True)
