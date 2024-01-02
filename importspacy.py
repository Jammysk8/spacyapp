import spacy
from spacy.matcher import Matcher
from numerizer import numerize
from spacy import load
import re
nlp = spacy.load("en_core_web_sm")

#Areas in Leeds to search in raw_text
leeds_areas = ["Adel", "Alwoodley", "Armley", "Austhorpe", "Beckhill", "Beeston", "Belle Isle", "Blenheim", "Bramley", "Burley",
               "Burmantofts", "Buslingthorpe", "The Calls", "Chapeltown", "Churwell", "Colton", "Cookridge", "Cottingley", "Crossgates", 
               "Eccup", "Fearnville", "Gipton", "Gledhow", "Halton", "Harehills", "Hawksworth", "Headingley",
               "Holbeck", "Hunslet", "Killingbeck", "Kirkstall", "Lawnswood", "Leylands", "Mabgate", "Manston",
               "Meanwood", "Middleton", "Moorside", "Moortown", "Oakwood", "Osmondthorpe", "Potternewton", "Rodley", "Roundhay",
               "Scotthall", "Seacroft", "Sheepscar", "Stourton", "Swarcliffe", "Swinnow", "Tinshill", "Weetwood",
               "Whinmoor", "Whitkirk", "Woodhouse", "Wortley", "Wykebeck"]

print(len(leeds_areas))


leeds_phraseareas = ["Arena Quarter", "Beckett Park",
                    "Beeston Hill", "Chapel Allerton", "Cottingley Towers and Cottingley Heights",
                    "Cross Gates", "East End Park", "Far Headingley", "Gamble Hill",
                    "Holbeck Urban Village", "Hunslet Grange Flats", "Ireland Wood", "Leeds city centre", "Lincoln Green",
                    "Little London", "Lovell Park", "Miles Hill", "Moor Allerton", "Moor Grange", "Pendas Fields", 
                    "Quarry Hill", "Scott Hall", "West Park"]

#Define patterns
location_pattern = [{"TEXT": area} for area in leeds_areas]
location_phrasepatten = [{"TEXT": areap} for areap in leeds_phraseareas]
amenities_pattern = [{"POS": "ADJ"}, {"POS": "NOUN"}]
features_pattern = [{"POS": "ADJ"}, {"POS": "NOUN"}]

property_features = [
   "double Bedroom", "Ensuite Bedroom", "Master Bedroom", "Guest Bedroom", "Nursery", "Walk-in Closet", "Built-in Wardrobes", "Dressing Room",
   "Family Bathroom", "Ensuite Bathroom", "Wet Room", "Guest Bathroom", "Jacuzzi Bath", "Walk-in Shower", "Power Shower", "Dual Sinks", "Heated Towel Rail",
   "Open Plan Living", "Lounge", "Dining Room", "Family Room", "Snug", "Study", "Playroom", "Utility Room", "Home Cinema", "Games Room",
   "Modern Kitchen", "Fitted Kitchen", "Gourmet Kitchen", "Breakfast Bar", "Integrated Appliances", "Dishwasher", "Washer Dryer", "Granite Worktops", "Island Unit", "Pantry",
   "Hardwood Flooring", "Tiled Flooring", "Underfloor Heating", "Stone Flooring", "Vinyl Flooring", "Wooden Beams", "Exposed Brickwork", "Feature Fireplace", "Sash Windows", 
   "Bay Windows", "Velux Windows", "French Doors", "Skylights", "Juliette Balcony", "Sliding Doors", "Conservatory",
   "Large Garden", "Enclosed Garden", "Landscaped Garden", "Patio", "Decking", "Sun Terrace", "BBQ Area", "Vegetable Patch", "Orchard", "Hot Tub",
   "Garage", "Off-Street Parking", "Driveway", "Secure Parking", "Double Garage", "Carport", "Electric Vehicle Charging Point", "Garage Storage",
   "Sea Views", "Mountain Views", "River Views", "City Views", "Countryside Views", "Panoramic Views", "Sunset Views", "Private Garden Views",
   "Cellar", "Conversion Potential", "Home Gym", "Cinema Room", "Wine Cellar",
   "Alarm System", "Gated Community", "CCTV", "Intercom System", "Secure Entry",
   "Solar Panels", "Eco-Friendly Heating", "Double Glazing", "Insulation", "A-Rated EPC",
   "Smart Home Features", "High-Speed Broadband", "Pet-Friendly", "Furnished", "No Onward Chain", "Close to Amenities", "Excellent Transport Links"
]

rent_priority_features_list = ["Double Glazing", "On street parking", "Basement", "Shed", "Attic", "garage", "garden", "rural"]
buyer_priority_features_list = ["Cellar", "loft conversion", "refurbished", "garden"]

nearby_list = ["Station", "train station", "primary school", "secondary school", "school", "shops", "high-street", "supermarket", "bus station", "park", "transit links"]
#property_types = ["House", "Semi-detached House", "Detached House", "Apartment", "Flat", "Mansion", "Maisonette", "Cottage", "Duplex Apartment", "Penthouse", "Studio Apartment", "Studio", "Studio Flat", "bungalow", "farm" ]

raw_text = """Double fronted houseDesirable location Walking distance to train station. Property. Property in Alwoodley.  Kitchen with integrated Bosch appliancesModern DesignTwo parking spacesDouble glazingGas central heatingMaster bedroom with ensuite showerEnclosed rear garden laid to lawn
Property description
A beautifully presented three bedroom detached property, situated in this popular new development, located on the former Tall Trees night club, with off street parking for two cars, garage and enclosed garden 
This spacious modern home is currently under construction(ready November) by Mulberry Homes Yorkshire Ltd and benefits from a highly efficient energy performance rating as well as a 10-year building warranty.
The property has been thoughtfully designed, briefly comprising of a living room, dining kitchen and with a large feature window and rear door leading to the garden and downstairs WC. On the first floor, there are three well sized bedrooms with the main bedroom benefitting from an ensuite shower room. There is also a modern house bathroom.
Arriving at the property you will find a block paved driveway with room for two vehicles. As well as a single garage with an up and over garage door, lighting, and power.
Upon entering the property, you will find a well-proportioned living room situated to the front of the property with full length ceiling to floor feature window.
Fantastic kitchen , ideal for growing families. The kitchen itself comprises a range of modern wall and base units with Bosch integrated appliances comprise of induction hob, electric oven, integrated fridge/ freezer, integrated dishwasher and integrated washing machine.
Downstairs WC with hand basin and under stairs storage cupboard Heading upstairs to the first floor, there are three good sized bedrooms.
The main bedroom benefits from an ensuite fitted with a walk-in shower unit, basin & vanity unit, WC and a chrome towel rail.
House bathroom with a modern white suite with WC, wash basin & vanity unit, bath with shower over and a glass shower screen.
Stepping outside to the rear of the property there is a level lawn garden as well as a patio area, ideal for outside dining with outside tap and double electric point."""

caption_templates = [
    
    """----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Check out this amazing {bed_no} bed property in {location}!🏡 It offers {found_features}.
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------""",
    #"Explore this fantastic place in {location} with {amenities} and {features}. 🌟\n",
    #"Discover this extraordinary property in {location},✨ it boasts {amenities} and presents {features}. 💯",
    #"Immerse yourself in this incredible abode in {location},🏡 it's equipped with {amenities} and infused with {features}. ✨",
    #"Unveiling an extraordinary haven in {location},💖✨ it's furnished with {amenities} and adorned with {features}. ✨",
    #"Experience the captivating charm of this property in {location},🏡✨ it serenades with {amenities} and mesmerizes with {features}. ✨",
    #"Embrace the exquisite elegance of this residence in {location},✨ it radiates with {amenities} and exudes {features}. ✨",
    #"Step into a breathtaking sanctuary in {location},💖✨ it's adorned with {amenities} and enriched with {features}. ✨",
    #"Discover a remarkable haven in {location},🏡✨ it's brimming with {amenities} and pulsating with {features}. ✨",
    #"Unleash your inner adventurer at this extraordinary property in {location},✨✨ it's equipped with {amenities} and teeming with {features}. ✨",
    #"Witness the splendor of this magnificent home in {location},🏡✨ it's a symphony of {amenities} and a canvas of {features}. ✨",
    #"Immerse yourself in the tranquil embrace of this property in {location},✨✨ it harmonizes with {amenities} and unfolds with {features}. ✨",
    #"Unveil the epitome of luxury in this extraordinary residence in {location},✨✨ it's a testament to {amenities} and a celebration of {features}. ✨",
    #"Embrace the spirit of wellness at this extraordinary property in {location},✨✨ it's infused with {amenities} and designed for {features}. ✨",
    #"Explore the endless possibilities at this incredible abode in {location},🏡✨✨ it's a tapestry of {amenities} and a landscape of {features}. ✨",
    #"Discover a haven of comfort and rejuvenation in this extraordinary property in {location},✨✨ it's a sanctuary of {amenities} and a haven of {features}. ✨",
    #"Unleash your creative spirit at this extraordinary property in {location},✨✨ it's a hub of {amenities} and a canvas for {features}. ✨",
    #"Immerse yourself in the heart of nature at this breathtaking property in {location},🏡✨✨ it's nestled among {amenities} and embraces {features}. ✨",
    #"Discover a timeless masterpiece in this extraordinary residence in {location},✨✨ it's a timeless blend of {amenities} and a masterpiece of {features}. ✨",
    #"Embrace the joy of family gatherings at this extraordinary property in {location},🏡✨✨ it's a haven for {amenities} and a backdrop for {features}. ✨",
    #"Unveil the essence of relaxation at this extraordinary haven in {location},✨✨ it's a sanctuary of {amenities} and a haven of {features}. ✨",
    #"Discover a haven of inspiration at this extraordinary property in {location},✨✨ it's a catalyst for {amenities} and a platform for {features}. ✨"
]

def find_areas_in_text(raw_text):
    #Process the input text using spaCy
    doc = nlp(raw_text)
    #Extract locations from the processed text
    found_areas=[]
    found_areas = [ent.text for ent in doc.ents if ent.text in leeds_areas[0:57]]
    print (found_areas)
    return found_areas
    
def find_bedrooms(raw_text):
    doc = nlp(raw_text)

    #Iterate over tokens in the document
    for token in doc:
        #Check if the token is a number and the next token contains "bedroom" or its variations
        if token.like_num and any(keyword in token.nbor(1).text.lower() for keyword in ["bed", "bedroom", "beds", "bedrooms"]):
            #Extract the number and return it
            bed_no = (token.text)
            bed_no = numerize(bed_no)
            return bed_no

def find_bathrooms(raw_text):
    #Process the input text using spaCy
    doc = nlp(raw_text)

    #Iterate over tokens in the document
    for token in doc:
        #Check if the token is a number and the next token contains "bedroom" or its variations
        if token.like_num and any(keyword in token.nbor(1).text.lower() for keyword in ["bathroom", "baths", "bathrooms"]):
            #Extract the number and return it
            bath_no = (token.text)
            return bath_no
     
     
def find_features(raw_text, property_type):
    #Process the input text using spaCy
    doc = nlp(raw_text)
    #Determine the priority features list based on the property type
    #priority_features_list = rent_priority_features_list if property_type.lower() == 'r' else buyer_priority_features_list

    #Initialize a spaCy Matcher
    matcher = Matcher(nlp.vocab)

    #Define a pattern for property features
    features_pattern = [{"LOWER": {"in": [feature.lower() for feature in property_features]}}]

    #Add the pattern to the matcher
    matcher.add("property_features", [features_pattern])

    #Initialize a list to store found features
    found_features = []

    #Apply the matcher to the document
    matches = matcher(doc)

    #Extract matched features
    for match_id, start, end in matches:
        feature_text = doc[start:end].text
        found_features.append(feature_text)

    #If the number of found features is less than the cap, search for additional non-duplicate features
    #additional_features = [feature.lower() for feature in priority_features_list if feature.lower() not in found_features]
    found_features = found_features[:5]  #Limit to the remaining needed features

    #Combine the found and additional features
    all_features = found_features
    all_features_set = set(all_features)
    #Add relevant descriptors and handle plural forms or phrases
    formatted_features = []
    for i, feature in enumerate(all_features_set):
        if " " in feature:
            formatted_features.append(feature)
        elif feature.endswith("s"):
            formatted_features.append(feature)
        elif feature[0] in "aeiou":
            formatted_features.append(f"an {feature}")
        else:
            formatted_features.append(f"a {feature}")

        #Check if it's the last item and add "and" before it
        if i == len(all_features_set) - 1:
            formatted_features[-1] = f"and {formatted_features[-1]}"

    print(formatted_features)
        #Join the features into a comma-separated string
    features_string = ', '.join(formatted_features)

    if not features_string:
        features_string = "No features found."

    print("Found features:", features_string)
    return features_string
property_type= "r"

def generate_social_media_caption(raw_text, property_type):
    #Find areas in the input text
    
    found_areas = find_areas_in_text(raw_text)
    beds = find_bedrooms(raw_text)
    baths = find_bathrooms(raw_text)
    feature = find_features(raw_text, property_type)
    #Create separate matcher objects for each type of information
    location_matcher = Matcher(nlp.vocab)
    amenities_matcher = Matcher(nlp.vocab)
    features_matcher = Matcher(nlp.vocab)


    #Add patterns to matchers
    location_matcher.add("location", [location_pattern])
    amenities_matcher.add("amenities", [amenities_pattern])
    features_matcher.add(".", [features_pattern])

    #Process raw text using spaCy
    doc = nlp(raw_text)

    #Extract location information
    location_matches = location_matcher(doc)

    #Assuming location_matches is a list of matches
    location_details = [doc[match[1]:match[2]].text.lower() for match in location_matches[:]]

    location_string = ', '.join(location_details + found_areas)  #Include found areas from spaCy entities

    #Extract amenities information
    amenities_matches = amenities_matcher(doc)
    amenities_details = [doc[match[1]:match[2]].text for match in amenities_matches[:5]]
    amenities_string = ', '.join(amenities_details)

    #Extract property features information
    features_matches = features_matcher(doc)
    features_details = [doc[match[1]:match[2]].text for match in features_matches[:5]]
    features_string = ', a'.join(features_details)

    caption = ''
    for template in caption_templates:
        cap = template.format(location=location_string.capitalize(), amenities=amenities_string, found_features = feature, bed_no = beds, bath_no = baths)
        caption += cap + '\n'
    return caption
    return property_type
caption = generate_social_media_caption(raw_text, property_type)
print(caption)