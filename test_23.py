import speech_recognition as sr
import pyttsx3

from pymongo import MongoClient

# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Function to speak text using pyttsx3
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# MongoDB connection setup
connection_string = ""
client = MongoClient(connection_string)
db = client["computer_shop"]
processor_collection = db["processor"]
gpu_collection = db["gpu"]

# Insert processor data if not present


# Check available components
def check_available_components(input_text):
    input_lower = input_text.lower()
    
    # Required keywords
    required_words = ["item", "component", "product"]
    
    # At least one of these words should be present
    availability_words = ["have", "available"]
    
    # Check if all required words are present
    required_present = any(word in input_lower for word in required_words)
    
    # Check if at least one availability word is present
    availability_present = any(word in input_lower for word in availability_words)
    
    if required_present and availability_present:
        return "We have GPUs and processors in the shop."
    else:
        return None

# Extract component type from user input
def extract_component_type(input_text):
    processor_keywords = ["processor", "cpu", "processors", "cpus"]
    gpu_keywords = ["gpu", "graphics card", "gpus", "graphic cards"]
    for word in input_text.lower().split():
        if word in processor_keywords:
            return "processor"
        elif word in gpu_keywords:
            return "gpu"
    return None

# Get price and details of a specific component
def get_price_and_details(input_text, component_type):
    if component_type == "processor":
        processor_type = extract_processor_type(input_text.lower())
        if processor_type:
            processor = processor_collection.find_one({"type": processor_type})
            if processor:
                if "price" in input_text.lower():
                    return f"The {processor_type} processor price is {processor['price']} rupees."
                elif "details" in input_text.lower():
                    return (f"The {processor_type} processor has a base clock of {processor['base_clock']} and {processor['cpu_cores']} CPU cores and {processor['threads']} threads. "
                            f"It has a {processor['warranty']} warranty period. You can buy this processor for {processor['price']} rupees.")
                else:
                    return "Sorry i did not understand. can you repeat the qeustion please"
    elif component_type == "gpu":
        gpu_model = extract_gpu_model(input_text.lower())
        if gpu_model:
            gpu = gpu_collection.find_one({"model": gpu_model})
            if gpu:
                if "price" in input_text.lower():
                    return f"The {gpu_model} GPU price is {gpu['price']} rupees."
                elif "details" in input_text.lower():
                    return (f"The {gpu_model} GPU has a boost clock of {gpu['boost_clock']} and {gpu['cuda_cores']} CUDA cores. "
                            f"The {gpu_model} GPU has {gpu['memory_type']} {gpu['memory_size']}. You can buy this GPU for {gpu['price']} rupees.")
                else:
                    return "Sorry i did not understand. can you repeat the qeustion please"
    return None

# Check availability of a component
def get_availability(input_text, component_type):
    input_lower = input_text.lower()
    availability_keywords = ["have", "available"]

    has_availability_keyword = any(keyword in input_lower for keyword in availability_keywords)

    if component_type == "processor" and has_availability_keyword:
        processors = list(processor_collection.find({}))
        if processors:
            result = "We have these processors in the shop:\n"
            for processor in processors:
                result += f" - {processor['type']}\n"
            return result.strip()
        else:
            return "We don't have any processors in stock at the moment."
        
    elif component_type == "gpu" and has_availability_keyword:
        gpus = list(gpu_collection.find({}))
        if gpus:
            result = "We have these graphic cards in the shop:\n"
            for gpu in gpus:
                result += f" - {gpu['model']}\n"
            return result.strip()
        else:
            return "We don't have any gpus in stock at the moment."

# Extract processor type from user input
def extract_processor_type(input_text):
    processor_types_mapping = {
        "intel core i five twelve four hundred": "INTEL CORE I5-12400",
        "i five twelve gen": "INTEL CORE I5-12400",
        "i5 12 gen": "INTEL CORE I5-12400",

        "amd ryzen nine seventy nine fifty x": "AMD RYZEN 9 7950X",
        "ryzen nine seventy nine fifty": "AMD RYZEN 9 7950X",
        "ryzen nine seven thousand nine hundred fifty": "AMD RYZEN 9 7950X",
        "ryzen 9 7950": "AMD RYZEN 9 7950X",

        "intel core i nine fourteen nine hundred k": "INTEL CORE I9 14900K",
        "i nine fourteen gen": "INTEL CORE I9 14900K",
        "i9 12 gen": "INTEL CORE I9 14900K",

        "intel core i seven twelve seven hundred": "INTEL CORE I7-12700",
        "i seven twelve gen": "INTEL CORE I7-12700",
        "i7 12 gen": "INTEL CORE I7-12700",

        "intel core i seven fourteen seven hundred k": "INTEL CORE I7 14700K",
        "i seven 14 gen": "INTEL CORE I7 14700K",
        "i7 14 gen": "INTEL CORE I7 14700K"
    }
    # Check pure English keywords
    for keyword, processor_type in processor_types_mapping.items():
        if keyword in input_text:
            return processor_type
    # Check original types
    for processor_type in ["INTEL CORE I5-12400", "AMD RYZEN 9 7950X", "INTEL CORE I9 14900K", "INTEL CORE I7-12700", "INTEL CORE I7 14700K"]:
        if processor_type.lower() in input_text:
            return processor_type
    return None

# Extract GPU model from user input
def extract_gpu_model(input_text):
    gpu_models_mapping = {
        "gtx sixteen sixty": "GTX 1660",
        "rtx twenty seventy": "RTX 2070",
        "rtx thirty eighty": "RTX 3080",
        "rx five eighty": "RX 580"
    }
    # Check pure English keywords
    for keyword, gpu_model in gpu_models_mapping.items():
        if keyword in input_text:
            return gpu_model
    # Check original types
    for gpu_model in ["GTX 1660", "RTX 2070", "RTX 3080", "RX 580"]:
        if gpu_model.lower() in input_text:
            return gpu_model
    return None

# Handle greetings
def handle_greetings(input_text):
    if "good morning" in input_text.lower():
        return "Good morning! How can I help you?"
    return None

# Handle gratitude
def handle_gratitude(input_text):
    if "thank you" in input_text.lower():
        return "Thank you for shopping. Come again!"
    return None

# Main conversation loop
while True:
    recognizer = sr.Recognizer()

    # Listen to user's speech input
    with sr.Microphone() as source:
        print("You: Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.listen(source)

    try:
        # Convert user's speech to text
        user_input = recognizer.recognize_google(audio_data)
        print("You:", user_input)

        # Handle greetings
        greeting_response = handle_greetings(user_input)
        if greeting_response:
            print("Bot:", greeting_response)
            speak_text(greeting_response)
            continue

        # Handle gratitude
        gratitude_response = handle_gratitude(user_input)
        if gratitude_response:
            print("Bot:", gratitude_response)
            speak_text(gratitude_response)
            continue

        # If not greetings or gratitude, proceed with component price query
        component_type = extract_component_type(user_input)

        available_components = check_available_components(user_input)
        if available_components:
            print("Bot:", available_components)
            speak_text(available_components)
        else:
            None

        price_and_details_response = get_price_and_details(user_input, component_type)
        if price_and_details_response:
            print("Bot:", price_and_details_response)
            speak_text(price_and_details_response)
        else:
            None

        availability_response = get_availability(user_input, component_type)
        if availability_response:
            print("Bot:", availability_response)
            speak_text(availability_response)
        else:
            None

    except sr.UnknownValueError:
        error_message = "Sorry, i could not understand you. can you repeat the question please"
        print("Bot:", error_message)
        speak_text(error_message)
    except sr.RequestError as e:
        error_message = f"Error occurred; {str(e)}"
        print("Bot:", error_message)
        speak_text(error_message)

    # Check if the user wants to end the conversation
    if user_input.lower() == "quit":
        farewell_message = "Goodbye!"
        print("Bot:", farewell_message)
        speak_text(farewell_message)
        break
