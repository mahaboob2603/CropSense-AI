import json

REMEDIES = {
    "Apple___Apple_scab": {
        "EN": {
            "disease_name": "Apple Scab",
            "crop": "Apple",
            "cause": "Fungus Venturia inaequalis. Thrives in cool, wet spring weather.",
            "symptoms": [
                "Olive-green to dull black velvety spots on leaves.",
                "Leaves may turn yellow and drop prematurely.",
                "Dark, scabby, rough spots on fruit causing deformities."
            ],
            "treatment_steps": [
                "Rake up and destroy fallen infected leaves to reduce overwintering spores.",
                "Prune trees to ensure good air circulation and sunlight penetration.",
                "Apply fungicides starting at silver tip or green tip growth stages."
            ],
            "organic_options": [
                "Liquid copper soap sprays applied early in the season.",
                "Sulfur or lime-sulfur sprays during pink bud stage.",
                "Neem oil as a preventative measure."
            ],
            "chemical_options": [
                "Captan 50 WP (2.5g/L water)",
                "Myclobutanil (Systhane) at recommended doses.",
                "Mancozeb 75 WP (2.5g/L water)"
            ],
            "prevention": [
                "Plant scab-resistant apple varieties (e.g., Honeycrisp, Liberty).",
                "Ensure proper orchard sanitation.",
                "Water at the base of trees, avoid wetting foliage."
            ]
        },
        "HI": {
            "disease_name": "सेब की पपड़ी (Apple Scab)",
            "crop": "सेब (Apple)",
            "cause": "कवक वेंटुरिया इनेक्वालिस। ठंडे और गीले वसंत के मौसम में पनपता है।",
            "symptoms": [
                "पत्तियों पर जैतून के हरे से लेकर सुस्त काले मखमली धब्बे।",
                "पत्तियां पीली होकर समय से पहले गिर सकती हैं।",
                "फलों पर गहरे, पपड़ीदार, खुरदरे धब्बे जिससे वे विकृत हो जाते हैं।"
            ],
            "treatment_steps": [
                "सर्दियों में छिपे बीजाणुओं को कम करने के लिए गिरी हुई संक्रमित पत्तियों को इकट्ठा कर नष्ट कर दें।",
                "पेड़ों की छंटाई करें ताकि हवा का प्रवाह और सूरज की रोशनी अच्छी तरह मिल सके।",
                "सिल्वर टिप या ग्रीन टिप विकास चरणों से ही कवकनाशी (fungicide) का प्रयोग शुरू करें।"
            ],
            "organic_options": [
                "सीजन की शुरुआत में तरल कॉपर साबुन का छिड़काव।",
                "पिंक बड (pink bud) चरण के दौरान सल्फर या लाइम-सल्फर का छिड़काव।",
                "बचाव के लिए नीम के तेल का प्रयोग।"
            ],
            "chemical_options": [
                "कैप्टन 50 WP (2.5 ग्राम/लीटर पानी)",
                "माइक्लोबुटानिल (सिस्टेन) अनुशंसित मात्रा में।",
                "मैंकोजेब 75 WP (2.5 ग्राम/लीटर पानी)"
            ],
            "prevention": [
                "स्कैब-प्रतिरोधी सेब की किस्में लगाएं (जैसे, हनीक्रिस्ट, लिबर्टी)।",
                "बगीचे में साफ-सफाई सुनिश्चित करें।",
                "पेड़ों की जड़ों में पानी दें, पत्तियों को गीला करने से बचें।"
            ]
        },
        "TE": {
            "disease_name": "ఆపిల్ స్కాబ్ (గజ్జి తెగులు)",
            "crop": "ఆపిల్ (Apple)",
            "cause": "వెంచురియా ఇనెక్వాలిస్ అనే ఫంగస్. చల్లని, తడి వసంత వాతావరణంలో పెరుగుతుంది.",
            "symptoms": [
                "ఆకులపై ఆలివ్-గ్రీన్ లేదా ముదురు నలుపు రంగు మచ్చలు.",
                "ఆకులు పసుపు రంగులోకి మారి అకాలంగా రాలిపోవచ్చు.",
                "పండ్ల మీద ముదురు, గొరిన, కఠినమైన మచ్చలు ఏర్పడి వికృతంగా మారుతాయి."
            ],
            "treatment_steps": [
                "కింద పడిన సోకిన ఆకులను సేకరించి కాల్చివేయండి.",
                "గాలి మరియు సూర్యరశ్మి బాగా తగిలేలా చెట్ల కొమ్మలను కత్తిరించండి.",
                "మొగ్గలు వచ్చే దశ నుండే ఫంగిసైడ్ (శిలీంద్రనాశిని) పిచికారీ ప్రారంభించండి."
            ],
            "organic_options": [
                "సీజన్ ప్రారంభంలో లిక్విడ్ కాపర్ సబ్బు ద్రావణాన్ని పిచికారీ చేయండి.",
                "పింక్ బడ్ దశలో సల్ఫర్ లేదా లైమ్-సల్ఫర్ పిచికారీ.",
                "నివారణ చర్యగా వేప నూనె వాడకం."
            ],
            "chemical_options": [
                "కెప్టాన్ 50 WP (2.5గ్రా/లీటరు నీటికి)",
                "మైక్లోబ్యూటానిల్ సిఫార్సు చేసిన మోతాదులో.",
                "మాంకోజెబ్ 75 WP (2.5గ్రా/లీటరు నీటికి)"
            ],
            "prevention": [
                "స్కాబ్-నిరోధక రకాలను ఎంచుకోండి.",
                "తోటలో పరిశుభ్రత పాటించండి.",
                "చెట్ల మొదళ్లలో మాత్రమే నీరు పెట్టండి, ఆకులపై నీరు పడకుండా చూడండి."
            ]
        }
    },
    "Apple___Black_rot": {
        "EN": {
            "disease_name": "Black Rot",
            "crop": "Apple",
            "cause": "Fungus Botryosphaeria obtusa. Enters through wounds or dead tissue.",
            "symptoms": [
                "Frog-eye leaf spots (purple margins with light centers).",
                "Sunken, reddish-brown to black cankers on branches.",
                "Firm, brown rotting spots on fruit eventually turning black and mummifying."
            ],
            "treatment_steps": [
                "Prune out dead or infected branches (cankers) at least 15 inches below the infection.",
                "Remove and destroy any mummified fruits from trees and the ground.",
                "Burn or bury all infected pruned material immediately."
            ],
            "organic_options": [
                "Copper-based fungicides applied before bud break.",
                "Maintain strict orchard hygiene."
            ],
            "chemical_options": [
                "Captan 50 WP applied from petal fall through summer.",
                "Thiophanate-methyl combined with Captan."
            ],
            "prevention": [
                "Avoid mechanical injury to bark.",
                "Remove dead wood annually during dormant pruning.",
                "Ensure trees are not stressed by drought or poor nutrition."
            ]
        },
        "HI": {
            "disease_name": "ब्लैक रॉट (काली सड़न)",
            "crop": "सेब (Apple)",
            "cause": "कवक बोट्रीओस्फेरिया ओब्टुसा। घावों या मृत ऊतकों के माध्यम से प्रवेश करता है।",
            "symptoms": [
                "पत्तियों पर मेंढक की आंख जैसे धब्बे (हल्के केंद्र के साथ बैंगनी किनारे)।",
                "शाखाओं पर धंसे हुए, लाल-भूरे से काले कैंकर (घाव)।",
                "फलों पर सख्त, भूरे रंग के सड़ने वाले धब्बे जो अंततः काले हो जाते हैं और ममीकृत हो जाते हैं।"
            ],
            "treatment_steps": [
                "संक्रमण से कम से कम 15 इंच नीचे मृत या संक्रमित शाखाओं (कैंकर) को काट कर हटा दें।",
                "पेड़ों और जमीन से किसी भी ममीकृत फल को हटा दें और नष्ट कर दें।",
                "सभी संक्रमित छंटाई सामग्री को तुरंत जला दें या गाड़ दें।"
            ],
            "organic_options": [
                "बड ब्रेक (कली खुलने) से पहले कॉपर-आधारित कवकनाशी का प्रयोग।",
                "बगीचे में सख्त स्वच्छता बनाए रखें।"
            ],
            "chemical_options": [
                "पंखुड़ी गिरने से लेकर गर्मियों तक कैप्टन 50 WP का प्रयोग।",
                "कैप्टन के साथ थियोफेनेट-मिथाइल।"
            ],
            "prevention": [
                "छाल को यांत्रिक चोट से बचाएं।",
                "सर्दियों में छंटाई के दौरान मृत लकड़ी को सालाना हटा दें।",
                "सुनिश्चित करें कि पेड़ सूखे या खराब पोषण से तनावग्रस्त न हों।"
            ]
        },
        "TE": {
            "disease_name": "బ్లాక్ రాట్ (నల్ల కుళ్ళు)",
            "crop": "ఆపిల్ (Apple)",
            "cause": "బోట్రియోస్ఫేరియా ఒబ్టుసా అనే ఫంగస్. గాయాలు లేదా చనిపోయిన కణజాలం ద్వారా ప్రవేశిస్తుంది.",
            "symptoms": [
                "ఆకులపై కప్ప కన్ను మచ్చలు (తెలుపు కేంద్రం, ఊదా అంచులు).",
                "కొమ్మలపై ముదురు ఎరుపు-గోధుమ లేదా నలుపు రంగు మచ్చలు/గాయాలు.",
                "పండ్ల మీద గోధుమ రంగు కుళ్ళు మచ్చలు ఏర్పడి, పండు నల్లగా మారుతుంది."
            ],
            "treatment_steps": [
                "వ్యాధి సోకిన కొమ్మలను వ్యాధి ఉన్న చోట కంటే 15 అంగుళాలు కిందకి కత్తిరించండి.",
                "చెట్లపై మరియు నేలపై ఉన్న కుళ్ళిన/ఎండిన పండ్లను తీసివేయండి.",
                "కత్తిరించిన కొమ్మలను వెంటనే కాల్చండి లేదా పూడ్చిపెట్టండి."
            ],
            "organic_options": [
                "మొగ్గలు రాకముందే కాపర్ ఆధారిత ఫంగిసైడ్ పిచికారీ.",
                "తోటలో పరిపూర్ణ పరిశుభ్రత పాటించడం."
            ],
            "chemical_options": [
                "పూత రాలుతున్న దశ నుండి కెప్టాన్ 50 WP వాడకం.",
                "కెప్టాన్ తో కలిపి థియోఫానేట్-మిథైల్."
            ],
            "prevention": [
                "చెట్ల బెరడుకు గాయాలు కాకుండా చూసుకోవాలి.",
                "ప్రతి ఏటా ఎండిన కొమ్మలను కత్తిరించాలి.",
                "చెట్లు నీటి ఎద్దడి వల్ల ఒత్తిడికి గురికాకుండా చూడాలి."
            ]
        }
    },
    "Apple___Cedar_apple_rust": {
        "EN": {
            "disease_name": "Cedar Apple Rust",
            "crop": "Apple",
            "cause": "Fungus Gymnosporangium juniperi-virginianae. Requires red cedar trees nearby to complete its life cycle.",
            "symptoms": [
                "Yellow-orange spots on leaves that enlarge and turn bright orange.",
                "Small, raised black dots appear in the center of the spots.",
                "Tubular structures develop on the underside of the leaves."
            ],
            "treatment_steps": [
                "Apply fungicides preventatively, as curative treatments are ineffective.",
                "Prune and destroy infected plant parts.",
                "Remove nearby red cedar trees if possible."
            ],
            "organic_options": [
                "Sulfur or copper-based fungicides applied during early spring.",
                "Neem oil spray."
            ],
            "chemical_options": [
                "Myclobutanil (Systhane) applied preventatively.",
                "Propiconazole (Tilt) during the growing season."
            ],
            "prevention": [
                "Plant rust-resistant apple varieties.",
                "Eradicate eastern red cedar trees within 1-2 miles of the orchard if possible."
            ]
        },
        "HI": {
            "disease_name": "सीडर एप्पल रस्ट",
            "crop": "सेब (Apple)",
            "cause": "जिम्नोस्पोरैंजियम ज्यूनिपेरी-वर्जिनियाने (Gymnosporangium juniperi-virginianae) कवक। इसके जीवन चक्र को पूरा करने के लिए पास में लाल देवदार के पेड़ों की आवश्यकता होती है।",
            "symptoms": [
                "पत्तियों पर पीले-नारंगी धब्बे जो बड़े होकर चमकीले नारंगी हो जाते हैं।",
                "धब्बों के बीच में छोटे, उभरे हुए काले बिंदु दिखाई देते हैं।",
                "पत्तियों के निचले हिस्से पर ट्यूबलर संरचनाएं विकसित होती हैं।"
            ],
            "treatment_steps": [
                "निवारक के तौर पर फफूंदनाशक का प्रयोग करें, क्योंकि उपचारात्मक उपचार ज्यादा काम नहीं करते।",
                "संक्रमित पौधों के हिस्सों को काट कर नष्ट कर दें।",
                "यदि संभव हो तो आसपास के लाल देवदार के पेड़ों को हटा दें।"
            ],
            "organic_options": [
                "शुरुआती वसंत के दौरान सल्फर या तांबे आधारित जैविक फफूंदनाशक का प्रयोग।",
                "नीम के तेल का स्प्रे।"
            ],
            "chemical_options": [
                "माइक्लोबूटानिल (Systhane) निवारक के रूप में।",
                "बढ़ते मौसम के दौरान प्रोपीकोनाजोल (Tilt)।"
            ],
            "prevention": [
                "रस्ट-प्रतिरोधी सेब की किस्में लगाएं।",
                "यदि संभव हो तो बगीचे के 1-2 मील के दायरे में लाल देवदार के पेड़ों को नष्ट कर दें।"
            ]
        },
        "TE": {
            "disease_name": "సెడార్ ఆపిల్ రస్ట్",
            "crop": "ఆపిల్ (Apple)",
            "cause": "జిమ్నోస్పోరాంజియం జునిపెరి-వర్జీనియానా ఫంగస్. దీని జీవిత చక్రం పూర్తి కావడానికి సమీపంలో సెడార్ (దేవదారు) చెట్లు అవసరం.",
            "symptoms": [
                "ఆకులపై పసుపు-నారింజ మచ్చలు, ఇవి పెద్దవిగా మరియు ముదురు నారింజ రంగులోకి మారుతాయి.",
                "మచ్చల మధ్యలో చిన్నగా ఉబ్బిన నల్లటి చుక్కలు కనిపిస్తాయి.",
                "ఆకుల కింది భాగంలో గొట్టాల (ట్యూబుల్స్) వంటి నిర్మాణాలు ఏర్పడతాయి."
            ],
            "treatment_steps": [
                "వ్యాధి సోకాక చికిత్స చేయడం కష్టం కాబట్టి, ముందుగానే ఫంగిసైడ్ పిచికారీ చేయాలి.",
                "వ్యాధి సోకిన ఆకులు/కొమ్మలను కత్తిరించి నాశనం చేయాలి.",
                "సమీపంలో ఉన్న సెడార్ చెట్లను తొలగించడం మంచిది."
            ],
            "organic_options": [
                "వసంతకాలం ప్రారంభంలో సల్ఫర్ లేదా కాపర్ ఆధారిత ఫంగిసైడ్స్ వాడకం.",
                "వేప నూనె పిచికారీ చూయాలి."
            ],
            "chemical_options": [
                "ముందుస్తుగా మైక్లోబ్యూటానిల్ స్థితులు.",
                "ప్రోపికొనజోల్ (టిల్ట్) పిచికారీ."
            ],
            "prevention": [
                "రస్ట్-నిరోధక రకాలను ఎంచుకోండి.",
                "సాధ్యమైతే తోట చుట్టూ 1-2 మైళ్లలో సెడార్ చెట్లను తొలగించండి."
            ]
        }
    },
    "Tomato___Early_blight": {
        "EN": {
            "disease_name": "Early Blight",
            "crop": "Tomato",
            "cause": "Fungus Alternaria solani. Favored by warm temperatures and high humidity/wet foliage.",
            "symptoms": [
                "Brown/black spots with target-like concentric rings on older, lower leaves.",
                "Yellowing surrounding the spots.",
                "Stem lesions and dark, sunken spots on fruit near the stem end."
            ],
            "treatment_steps": [
                "Remove and destroy infected lower leaves immediately.",
                "Apply mulch around the base of the plant to prevent soil-borne spores from splashing onto leaves.",
                "Apply appropriate fungicides as soon as symptoms appear."
            ],
            "organic_options": [
                "Copper-based organic fungicides (e.g., Copper fungicide soap).",
                "Bacillus subtilis biological fungicide.",
                "Baking soda spray (1 tbsp baking soda + 1 tsp soap per gallon of water)."
            ],
            "chemical_options": [
                "Chlorothalonil (e.g., Daconil) applied every 7-10 days.",
                "Mancozeb 75% WP (2-2.5g/L of water).",
                "Azoxystrobin (systemic fungicide)."
            ],
            "prevention": [
                "Rotate crops; do not plant tomatoes or potatoes in the same spot for 2-3 years.",
                "Space plants properly to ensure adequate airflow and quick drying of leaves.",
                "Use drip irrigation or water at the base to keep leaves dry."
            ]
        },
        "HI": {
            "disease_name": "अर्ली ब्लाइट (अगेती झुलसा)",
            "crop": "टमाटर (Tomato)",
            "cause": "कवक अल्टरनेरिया सोलानी। गर्म तापमान और उच्च आर्द्रता/गीली पत्तियों द्वारा अनुकूल।",
            "symptoms": [
                "पुरानी, निचली पत्तियों पर लक्ष्य (target) जैसे संकेंद्रित छल्लों के साथ भूरे/काले धब्बे।",
                "धब्बों के आसपास पीलापन।",
                "तने पर घाव और फल के तने वाले सिरे के पास गहरे, धंसे हुए धब्बे।"
            ],
            "treatment_steps": [
                "संक्रमित निचली पत्तियों को तुरंत हटा दें और नष्ट कर दें।",
                "मिट्टी जनित बीजाणुओं को पत्तियों पर छलकने से रोकने के लिए पौधे के आधार के चारों ओर मल्च (पुआल/पन्नी) लगाएं।",
                "लक्षण दिखाई देते ही उचित कवकनाशी का प्रयोग करें।"
            ],
            "organic_options": [
                "कॉपर-आधारित जैविक कवकनाशी।",
                "बैसिलस सबटिलिस जैविक कवकनाशी।",
                "बेकिंग सोडा स्प्रे (1 बड़ा चम्मच बेकिंग सोडा + 1 चम्मच साबुन प्रति गैलन पानी)।"
            ],
            "chemical_options": [
                "क्लोरोथालोनिल हर 7-10 दिनों में लगाया जाता है।",
                "मैंकोजेब 75% WP (2-2.5 ग्राम/लीटर पानी)।",
                "एज़ोक्सीस्ट्रोबिन (सिस्टमैटिक फफूंदनाशक)।"
            ],
            "prevention": [
                "फसल चक्र अपनाएं; 2-3 वर्षों तक एक ही स्थान पर टमाटर या आलू न लगाएं।",
                "हवा के समुचित प्रवाह और पत्तियों के जल्दी सूखने को सुनिश्चित करने के लिए पौधों के बीच उचित दूरी रखें।",
                "पत्तियों को सूखा रखने के लिए ड्रिप सिंचाई या आधार पर पानी का उपयोग करें।"
            ]
        },
        "TE": {
            "disease_name": "ఎర్లీ బ్లైట్ (ముందస్తు ఆకుమాడు తెగులు)",
            "crop": "టమాటా (Tomato)",
            "cause": "ఆల్టర్నేరియా సోలాని అనే ఫంగస్. వెచ్చని ఉష్ణోగ్రతలు మరియు అధిక తేమ వల్ల వ్యాపిస్తుంది.",
            "symptoms": [
                "పాత, కింది ఆకులపై గుండ్రటి వలయాలతో గోధుమ/నలుపు మచ్చలు.",
                "మచ్చల చుట్టూ ఆకులు పసుపు రంగులోకి మారడం.",
                "కాండం మీద గాయాలు మరియు పండు తొడిమ దగ్గర ముదురు మచ్చలు."
            ],
            "treatment_steps": [
                "వ్యాధి సోకిన కింది ఆకులను వెంటనే తొలగించి నాశనం చేయాలి.",
                "మట్టిలోని ఫంగస్ ఆకులపై పడకుండా మొక్కల మొదళ్ల చుట్టూ మల్చింగ్ (గడ్డి/ప్లాస్టిక్) వేయాలి.",
                "లక్షణాలు కనిపించిన వెంటనే ఫంగిసైడ్ పిచికారీ చేయాలి."
            ],
            "organic_options": [
                "కాపర్ ఆధారిత ఆర్గానిక్ ఫంగిసైడ్స్ వాడకం.",
                "బాసిల్లస్ సబ్టిలిస్ (జీవ శిలీంద్రనాశిని).",
                "బేకింగ్ సోడా ద్రావణం (1 టీస్పూన్+సబ్బు పౌడర్)."
            ],
            "chemical_options": [
                "క్లోరోథలోనిల్ (Daconil) ప్రతి 7-10 రోజులకు.",
                "మాంకోజెబ్ 75% WP (2-2.5 గ్రా/లీటరు).",
                "అజోక్సీస్ట్రోబిన్ వాడకం."
            ],
            "prevention": [
                "పంట మార్పిడి చేయాలి; 2-3 ఏళ్ల పాటు ఒకే చోట టమాటా/బంగాళదుంప వేయరాదు.",
                "గాలి బాగా ఆడేలా మొక్కల మధ్య తగినంత దూరం ఉంచాలి.",
                "ఆకులు తడవకుండా డ్రిప్ ఇరిగేషన్ లేదా మొదళ్లలో నీరు పోయాలి."
            ]
        }
    },
    "Tomato___Late_blight": {
        "EN": {
            "disease_name": "Late Blight",
            "crop": "Tomato",
            "cause": "Oomycete Phytophthora infestans. Thrives in cool, extremely wet/humid weather. Highly contagious.",
            "symptoms": [
                "Large, dark, water-soaked patches on leaves that grow rapidly.",
                "White fuzzy fungal growth on the underside of leaves during humid conditions.",
                "Dark brown/black firm spots on green or ripe fruit.",
                "Rapid collapse of the entire plant (blighting)."
            ],
            "treatment_steps": [
                "IMMEDIATE ACTION REQUIRED. Dig up and destroy heavily infected plants by bagging and trashing or burning.",
                "DO NOT compost infected plants as the pathogen can survive and spread.",
                "Apply systemic fungicides to surrounding apparently healthy plants."
            ],
            "organic_options": [
                "Preventative copper sprays are the ONLY viable organic option, but they are ineffective once severe infection starts."
            ],
            "chemical_options": [
                "Cymoxanil + Mancozeb mix.",
                "Mefenoxam or Metalaxyl-based systemic fungicides.",
                "Dimethomorph + Mancozeb formulations."
            ],
            "prevention": [
                "Plant late blight-resistant varieties (e.g., Mountain Magic, Defiant).",
                "Eliminate all volunteer tomato and potato plants from previous seasons.",
                "Ensure maximum airflow and strictly avoid wetting foliage."
            ]
        },
        "HI": {
            "disease_name": "लेट ब्लाइट (पछेती झुलसा)",
            "crop": "टमाटर (Tomato)",
            "cause": "फाइटोफ्थोरा इन्फेस्टैन्स। ठंडे, अत्यधिक गीले/आर्द्र मौसम में पनपता है। अत्यधिक संक्रामक।",
            "symptoms": [
                "पत्तियों पर बड़े, गहरे, पानी से भीगे हुए धब्बे जो तेजी से बढ़ते हैं।",
                "नम स्थिति में पत्तियों के निचले हिस्से पर सफेद फजी कवक वृद्धि।",
                "हरे या पके फल पर गहरे भूरे/काले सख्त धब्बे।",
                "पूरे पौधे का तेजी से नष्ट होना (झुलसना)।"
            ],
            "treatment_steps": [
                "तत्काल कार्रवाई आवश्यक। भारी रूप से संक्रमित पौधों को उखाड़ कर पॉलीबैग में पूरी तरह बंद कर कचरे में फेंक दें या जला दें।",
                "संक्रमित पौधों को खाद (कम्पोस्ट) में न डालें क्योंकि रोगज़नक़ जीवित रह सकते हैं।",
                "आसपास के स्वस्थ दिखने वाले पौधों पर तुरंत सिस्टमैटिक कवकनाशी का प्रयोग करें।"
            ],
            "organic_options": [
                "रोकथाम के लिए कॉपर स्प्रे ही एकमात्र व्यवहार्य जैविक विकल्प है, लेकिन गंभीर संक्रमण होने के बाद वे अप्रभावी होते हैं।"
            ],
            "chemical_options": [
                "साइमोक्सानिल + मैंकोजेब (Cymoxanil + Mancozeb) मिश्रण।",
                "मेफेनोक्सम या मेटलैक्सिल-आधारित कवकनाशी।",
                "डाइमेथोमोर्फ + मैंकोजेब 50% डब्ल्यूपी।"
            ],
            "prevention": [
                "लेट ब्लाइट-प्रतिरोधी किस्में लगाएं।",
                "पिछले मौसमों के सभी स्वैच्छिक (अपने आप उगे हुए) टमाटर और आलू के पौधों को नष्ट करें।",
                "अधिकतम वायु प्रवाह सुनिश्चित करें और पत्तियों को गीला होने से पूरी तरह बचाएं।"
            ]
        },
        "TE": {
            "disease_name": "లేట్ బ్లైట్ (లేటు ఆకుమాడు తెగులు/నల్లమచ్చ తెగులు)",
            "crop": "టమాటా (Tomato)",
            "cause": "ఫైటోఫ్తోరా ఇన్ఫెస్టాన్స్. చల్లని, అధిక తేమతో కూడిన వాతావరణంలో వేగంగా వ్యాపిస్తుంది. అత్యంత ప్రమాదకరం.",
            "symptoms": [
                "ఆకులపై నీటితో నిండిన పెద్ద, ముదురు మచ్చలు వేగంగా పక్కకు వ్యాపిస్తాయి.",
                "తేమ వాతావరణంలో ఆకుల అడుగున తెల్లటి శిలీంద్రపు పొర ఏర్పడుతుంది.",
                "ఆకుపచ్చ లేదా పక్వానికి వచ్చిన పండ్ల మీద ముదురు గోధుమ/నలుపు గట్టి మచ్చలు రావడం.",
                "మొక్క మొత్తం వేగంగా కుళ్ళిపోవడం."
            ],
            "treatment_steps": [
                "తక్షణ చర్య అవసరం! వ్యాధి సోకిన మొక్కలను పీకి, కవర్లో బంధించి దూరంగా పడేయాలి లేదా కాల్చేయాలి.",
                "వ్యాధిగ్రస్తులైన మొక్కలతో కంపోస్ట్ ఎరువు చేయకూడదు.",
                "చుట్టుపక్కల ఆరోగ్యంగా ఉన్న మొక్కలకు వెంటనే రక్షణగా ఫంగిసైడ్ పిచికారీ చేయాలి."
            ],
            "organic_options": [
                "ముందుస్తుగా కాపర్ పిచికారీ చేయడం మాత్రమే సేంద్రియ మార్గం. వ్యాధి ముదిరితే ఆర్గానిక్ మందులు బాగో పనిచేయవు."
            ],
            "chemical_options": [
                "సైమోక్సానిల్ + మాంకోజెబ్ మిశ్రమం.",
                "మెటలాక్సిల్ 8% + మాంకోజెబ్ 64% WP (రిడోమిల్ గోల్డ్) పిచికారీ.",
                "డైమెథోమోర్ఫ్ + మాంకోజెబ్."
            ],
            "prevention": [
                "లేట్ బ్లైట్ తట్టుకునే రకాలను నాటండి.",
                "పాత పంట నుండి మిగిలిపోయిన లేదా దానంతట అదే మొలచిన టమాటా/బంగాళదుంప మొక్కలను పీకేయండి.",
                "గాలి ప్రసరణ బాగా ఉండేలా చూడండి, ఆకులు తడవకుండా కాపాడండి."
            ]
        }
    },
    "Tomato___Bacterial_spot": {
        "EN": {
            "disease_name": "Bacterial Spot",
            "crop": "Tomato",
            "cause": "Bacterium Xanthomonas campestris pv. vesicatoria. Splashed by rain and overhead watering.",
            "symptoms": [
                "Small, water-soaked, greasy-looking spots on leaves and stems.",
                "Spots eventually turn black and are accompanied by a yellow halo.",
                "Scabby, dark raised spots on green and ripe fruit."
            ],
            "treatment_steps": [
                "There is no cure for bacterial spot on severely infected plants; they should be removed and destroyed.",
                "Do not compost infected plants.",
                "Apply copper-based sprays early in the infection cycle to slow spread."
            ],
            "organic_options": [
                "Copper fungicide applied as a preventative spray.",
                "Bacillus subtilis to suppress bacterial spread."
            ],
            "chemical_options": [
                "Copper fungicides mixed with mancozeb for better control.",
                "Streptomycin sprays (where legally permitted and not resistant)."
            ],
            "prevention": [
                "Use certified disease-free seeds and transplants.",
                "Use drip irrigation to keep foliage dry.",
                "Mulch to prevent soil from splashing onto lower leaves."
            ]
        },
        "HI": {
            "disease_name": "बैक्टीरियल स्पॉट (जीवाणु धब्बा)",
            "crop": "टमाटर (Tomato)",
            "cause": "ज़ैंथोमोनस कैंपेस्ट्रिस (Xanthomonas campestris pv. vesicatoria) बैक्टीरिया। बारिश और ऊपर से पानी देने से फैलता है।",
            "symptoms": [
                "पत्तियों और तनों पर छोटे, पानी से भीगे हुए, चिकने दिखने वाले धब्बे।",
                "धब्बे अंततः काले हो जाते हैं और उनके चारों ओर पीला घेरा (halo) बन जाता है।",
                "हरे और पके फलों पर पपड़ीदार, गहरे उभरे हुए धब्बे।"
            ],
            "treatment_steps": [
                "गंभीर रूप से संक्रमित पौधों के लिए कोई इलाज नहीं है; उन्हें हटा दिया जाना चाहिए और नष्ट कर दिया जाना चाहिए।",
                "संक्रमित पौधों को कम्पोस्ट (खाद) में न डालें।",
                "फैलने से रोकने के लिए संक्रमण चक्र की शुरुआत में कॉपर-आधारित स्प्रे लागू करें।"
            ],
            "organic_options": [
                "निवारक स्प्रे के रूप में कॉपर कवकनाशी का प्रयोग।",
                "बैक्टीरिया के प्रसार को दबाने के लिए बैसिलस सबटिलिस।"
            ],
            "chemical_options": [
                "बेहतर नियंत्रण के लिए मैंकोजेब (Mancozeb) के साथ मिश्रित कॉपर कवकनाशी।",
                "स्ट्रेप्टोमाइसिन स्प्रे (जहां कानूनी रूप से अनुमति है)।"
            ],
            "prevention": [
                "प्रमाणित रोग-मुक्त बीज और पौधों का उपयोग करें।",
                "पत्तियों को सूखा रखने के लिए ड्रिप सिंचाई का उपयोग करें।",
                "निचली पत्तियों पर मिट्टी के छींटों को रोकने के लिए मल्चिंग करें।"
            ]
        },
        "TE": {
            "disease_name": "బాక్టీరియల్ స్పాట్",
            "crop": "టమాటా (Tomato)",
            "cause": "క్సాంతోమోనాస్ కాంపెస్ట్రిస్ (Xanthomonas) బాక్టీరియా. వర్షం మరియు పైనుండి నీరు పోయడం వల్ల వ్యాపిస్తుంది.",
            "symptoms": [
                "ఆకులు, కాండంపై చిన్నగా, నీరు పట్టినట్లుజిడ్డుగా ఉండే మచ్చలు.",
                "మచ్చల చుట్టూ పసుపు రంగు వలయం ఏర్పడి నల్లగా మారుతాయి.",
                "ఆకుపచ్చ మరియు పండిన పండ్ల మీద గట్టిపడిన నలుపు మచ్చలు."
            ],
            "treatment_steps": [
                "వ్యాధి తీవ్రంగా ఉన్న మొక్కలకు చికిత్స లేదు; వాటిని వేరుతో సహా పీకి నాశనం చేయాలి.",
                "వ్యాధి సోకిన మొక్కలతో కంపోస్ట్ చేయకూడదు.",
                "వ్యాధి ఇప్పుడే మొదలవుతుంటే కాపర్ (రాగి) ఆధారిత మందులను పిచికారీ చేయాలి."
            ],
            "organic_options": [
                "ముందుస్తుగా కాపర్ ఫంగిసైడ్ పిచికారీ.",
                "బాక్టీరియా వ్యాప్తిని అరికట్టడానికి బాసిల్లస్ సబ్టిలిస్."
            ],
            "chemical_options": [
                "మరింత మెరుగైన నియంత్రణ కోసం కాపర్ మందులతో పాటు మాంకోజెబ్ కలిపి వాడాలి.",
                "స్ట్రెప్టోమైసిన్ పిచికారీ (సిఫారసు చేసిన మేరకు చూసి వాడాలి)."
            ],
            "prevention": [
                "ధృవీకరించబడిన వ్యాధి-రహిత విత్తనాలు మరియు నారును ఉపయోగించండి.",
                "ఆకులు తడవకుండా డ్రిప్ ఇరిగేషన్ వాడండి.",
                "కింది ఆకులపై మట్టి పడకుండా మల్చింగ్ వేయండి."
            ]
        }
    },
    "Tomato___healthy": {
        "EN": {
            "disease_name": "Healthy",
            "crop": "Tomato",
            "cause": "Plant is currently free from visible diseases.",
            "symptoms": [
                "Green, vibrant foliage.",
                "No visible spots or lesions.",
                "Steady growth and fruiting."
            ],
            "treatment_steps": [
                "No specific treatment required. Continue regular maintenance."
            ],
            "organic_options": [
                "Continue compost teas and organic fertilizers for soil health."
            ],
            "chemical_options": [
                "Not applicable."
            ],
            "prevention": [
                "Maintain consistent watering to prevent blossom end rot.",
                "Apply balanced fertilizer (like 5-10-10) when flowers appear.",
                "Stake or cage plants to keep foliage off the damp ground."
            ]
        },
        "HI": {
            "disease_name": "स्वस्थ",
            "crop": "टमाटर (Tomato)",
            "cause": "पौधा वर्तमान में दृश्यमान बीमारियों से मुक्त है।",
            "symptoms": [
                "हरी, जीवंत पत्तियां।",
                "कोई दिखाई देने वाले धब्बे या घाव नहीं।",
                "स्थिर वृद्धि और फलन।"
            ],
            "treatment_steps": [
                "किसी विशेष उपचार की आवश्यकता नहीं है। नियमित रखरखाव जारी रखें।"
            ],
            "organic_options": [
                "मिट्टी के स्वास्थ्य के लिए कम्पोस्ट टी और जैविक खाद जारी रखें।"
            ],
            "chemical_options": [
                "लागू नहीं।"
            ],
            "prevention": [
                "ब्लोसम एंड रॉट से बचने के लिए लगातार पानी दें।",
                "फूल आने पर संतुलित उर्वरक (जैसे 5-10-10) डालें।",
                "पत्तियों को नम जमीन से दूर रखने के लिए पौधों को सहारा दें (स्टेकिंग)।"
            ]
        },
        "TE": {
            "disease_name": "ఆరోగ్యవంతమైనది",
            "crop": "టమాటా (Tomato)",
            "cause": "మొక్క ప్రస్తుతం ఎటువంటి కంటికి కనిపించే వ్యాధుల్లేకుండా ఆరోగ్యంగా ఉంది.",
            "symptoms": [
                "ఆకుపచ్చని, చురుకైన ఆకులు.",
                "మచ్చలు లేదా గాయాలు లేకపోవడం.",
                "స్థిరమైన ఎదుగుదల మరియు కాయలు కాయడం."
            ],
            "treatment_steps": [
                "ఎటువంటి ప్రత్యేక చికిత్స అవసరం లేదు. సాధారణ సంరక్షణ కొనసాగించండి."
            ],
            "organic_options": [
                "నేల ఆరోగ్యం కోసం సేంద్రియ ఎరువులు మరియు వర్మీ కంపోస్ట్ వాడటం కొనసాగించండి."
            ],
            "chemical_options": [
                "వర్తించదు."
            ],
            "prevention": [
                "బ్లోసమ్ ఎండ్ రాట్ నివారించడానికి క్రమం తప్పకుండా ఒకే మోతాదులో నీరు పెట్టండి.",
                "పూత దశలో సమతుల్య ఎరువులు (5-10-10 లాంటివి) వాడండి.",
                "ఆకులు నేలకు తగలకుండా మొక్కలకు కర్రలు లేదా జాలి సహాయంతో దన్ను కట్టండి."
            ]
        }
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "EN": {
            "disease_name": "Cherry Powdery Mildew",
            "crop": "Cherry",
            "cause": "Fungus Podosphaera clandestina. Favors warm, dry days with cool nights.",
            "symptoms": [
                "White powdery coating on young leaves and shoots.",
                "Leaf curling and stunted shoot growth.",
                "Fruit may develop superficial blemishes."
            ],
            "treatment_steps": [
                "Remove and destroy infected shoots during dormant pruning.",
                "Apply sulfur-based fungicide at petal fall.",
                "Ensure good air circulation by thinning canopy."
            ],
            "organic_options": [
                "Potassium bicarbonate spray (3g/L).",
                "Neem oil applied at 7-day intervals.",
                "Milk spray (1:9 ratio with water)."
            ],
            "chemical_options": [
                "Myclobutanil (Rally) at label rate.",
                "Trifloxystrobin (Flint) preventively.",
                "Sulfur 80 WP (3g/L water)."
            ],
            "prevention": [
                "Plant resistant cherry cultivars.",
                "Avoid overhead irrigation.",
                "Prune for open canopy structure."
            ]
        },
        "HI": {
            "disease_name": "चेरी का चूर्णिल आसिता",
            "crop": "चेरी",
            "cause": "कवक पोडोस्फेरा क्लैंडेस्टिना (Podosphaera clandestina) के कारण होता है। गर्म, शुष्क दिन और ठंडी रातें इसके लिए अनुकूल होती हैं।",
            "symptoms": [
                "युवा पत्तियों और अंकुरों पर सफेद चूर्ण जैसा लेप।",
                "पत्तियों का मुड़ना और अंकुरों का अवरुद्ध विकास।",
                "फलों पर ऊपरी सतह पर दाग-धब्बे पड़ सकते हैं।"
            ],
            "treatment_steps": [
                "सुषुप्त अवस्था में छंटाई के दौरान संक्रमित अंकुरों को हटाकर नष्ट करें।",
                "पंखुड़ी गिरने पर सल्फर-आधारित फफूंदनाशक का प्रयोग करें।",
                "छतरी को पतला करके हवा का अच्छा संचार सुनिश्चित करें।"
            ],
            "organic_options": [
                "पोटेशियम बाइकार्बोनेट का छिड़काव (3 ग्राम/लीटर)।",
                "7 दिनों के अंतराल पर नीम के तेल का प्रयोग करें।",
                "दूध का छिड़काव (पानी के साथ 1:9 के अनुपात में)।"
            ],
            "chemical_options": [
                "माइक्लोब्यूटानिल (रैली) का लेबल दर पर प्रयोग करें।",
                "ट्राइफ्लॉक्सिस्ट्रोबिन (फ्लिंट) का निवारक रूप से प्रयोग करें।",
                "सल्फर 80 डब्ल्यू पी (3 ग्राम/लीटर पानी) का प्रयोग करें।"
            ],
            "prevention": [
                "प्रतिरोधी चेरी किस्मों को लगाएं।",
                "ऊपरी सिंचाई से बचें।",
                "खुली छतरी संरचना के लिए छंटाई करें।"
            ]
        },
        "TE": {
            "disease_name": "చెర్రీ బూడిద తెగులు",
            "crop": "చెర్రీ",
            "cause": "పోడోస్ఫెరా క్లాండెస్టైనా అనే శిలీంధ్రం వలన వస్తుంది. వెచ్చని, పొడి రోజులు మరియు చల్లని రాత్రులు దీనికి అనుకూలం.",
            "symptoms": [
                "లేత ఆకులు మరియు చిగుళ్ళపై తెల్లటి బూడిద పూత.",
                "ఆకులు ముడుచుకుపోవడం మరియు చిగుళ్ళ పెరుగుదల మందగించడం.",
                "పండ్లపై పైపైన మచ్చలు ఏర్పడవచ్చు."
            ],
            "treatment_steps": [
                "చెట్లు నిద్రాణ స్థితిలో ఉన్నప్పుడు కత్తిరించేటప్పుడు సోకిన చిగుళ్ళను తొలగించి నాశనం చేయండి.",
                "పూల రేకులు రాలిన తర్వాత సల్ఫర్ ఆధారిత శిలీంధ్రనాశకాన్ని పిచికారీ చేయండి.",
                "చెట్ల కొమ్మలను పల్చబరచడం ద్వారా మంచి గాలి ప్రసరణను నిర్ధారించుకోండి."
            ],
            "organic_options": [
                "పొటాషియం బైకార్బోనేట్ పిచికారీ (3 గ్రా/లీ).",
                "7 రోజుల వ్యవధిలో వేప నూనెను పిచికారీ చేయండి.",
                "పాలు పిచికారీ (నీటితో 1:9 నిష్పత్తిలో)."
            ],
            "chemical_options": [
                "మైక్లోబుటానిల్ (రాలీ) లేబుల్ సూచించిన మోతాదులో.",
                "ట్రైఫ్లోక్సిస్ట్రోబిన్ (ఫ్లింట్) నివారణగా.",
                "సల్ఫర్ 80 WP (3 గ్రా/లీ నీటిలో)."
            ],
            "prevention": [
                "తెగులు నిరోధక చెర్రీ రకాలను నాటండి.",
                "తల పై నుండి నీటిపారుదలను నివారించండి.",
                "గాలి తగిలేలా పందిరిని కత్తిరించండి."
            ]
        }
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "EN": {
            "disease_name": "Corn Gray Leaf Spot",
            "crop": "Corn (Maize)",
            "cause": "Fungus Cercospora zeae-maydis. Thrives in warm, humid conditions with poor air flow.",
            "symptoms": [
                "Rectangular, gray to tan lesions between leaf veins.",
                "Lesions may coalesce causing large dead areas.",
                "Severe infections lead to premature leaf death."
            ],
            "treatment_steps": [
                "Rotate corn with non-host crops (soybean, wheat).",
                "Till crop residue to reduce inoculum.",
                "Apply foliar fungicide at VT-R1 growth stage."
            ],
            "organic_options": [
                "Bacillus subtilis biological fungicide.",
                "Trichoderma-based soil amendments.",
                "Compost tea foliar spray."
            ],
            "chemical_options": [
                "Azoxystrobin (Quadris) at 200ml/acre.",
                "Propiconazole (Tilt) at recommended rate.",
                "Pyraclostrobin + Metconazole combination."
            ],
            "prevention": [
                "Plant gray leaf spot resistant hybrids.",
                "Avoid continuous corn planting.",
                "Maintain proper plant spacing."
            ]
        },
        "HI": {
            "disease_name": "मक्का का धूसर पत्ती धब्बा",
            "crop": "मक्का",
            "cause": "सर्कोस्पोरा ज़ी-मेडीस कवक के कारण। यह गर्म, आर्द्र परिस्थितियों और खराब वायु संचार वाले स्थानों में पनपता है।",
            "symptoms": [
                "पत्ती की शिराओं के बीच आयताकार, धूसर से हल्के भूरे रंग के धब्बे।",
                "धब्बे आपस में मिलकर बड़े मृत क्षेत्र बना सकते हैं।",
                "गंभीर संक्रमण से पत्तियां समय से पहले मर जाती हैं।"
            ],
            "treatment_steps": [
                "गैर-मेजबान फसलों (जैसे सोयाबीन, गेहूं) के साथ मक्के की फसल का चक्रीकरण करें।",
                "रोगजनक को कम करने के लिए फसल अवशेषों को जुताई करके मिट्टी में मिलाएं।",
                "वीटी-आर1 वृद्धि अवस्था पर पत्तियों पर फफूंदनाशक का छिड़काव करें।"
            ],
            "organic_options": [
                "बैसिलस सबटिलिस जैविक फफूंदनाशक।",
                "ट्राइकोडर्मा-आधारित मृदा सुधारक।",
                "कम्पोस्ट चाय का पत्तियों पर छिड़काव।"
            ],
            "chemical_options": [
                "एज़ॉक्सिस्ट्रोबिन (क्वाड्रिस) 200 मिली/एकड़ की दर से।",
                "प्रोपीकोनाज़ोल (टिल्ट) सिफारिश की गई दर पर।",
                "पाइराक्लोस्ट्रोबिन + मेटकोनाज़ोल का संयोजन।"
            ],
            "prevention": [
                "धूसर पत्ती धब्बा प्रतिरोधी संकर किस्में लगाएं।",
                "लगातार मक्का बोने से बचें।",
                "पौधों के बीच उचित दूरी बनाए रखें।"
            ]
        },
        "TE": {
            "disease_name": "మొక్కజొన్న బూడిద ఆకు మచ్చ",
            "crop": "మొక్కజొన్న",
            "cause": "సెర్కోస్పోరా జియే-మేడిస్ అనే శిలీంధ్రం వలన వస్తుంది. వెచ్చని, తేమతో కూడిన వాతావరణం మరియు తక్కువ గాలి ప్రసరణ ఉన్న చోట ఇది వృద్ధి చెందుతుంది.",
            "symptoms": [
                "ఆకు ఈనెల మధ్య దీర్ఘచతురస్రాకార, బూడిద నుండి లేత గోధుమ రంగు మచ్చలు.",
                "మచ్చలు కలిసిపోయి పెద్ద చనిపోయిన ప్రాంతాలను ఏర్పరచవచ్చు.",
                "తీవ్రమైన ఇన్ఫెక్షన్లు ఆకులు ముందుగానే చనిపోవడానికి దారితీస్తాయి."
            ],
            "treatment_steps": [
                "మొక్కజొన్నను ఈ తెగులును ఆశ్రయించని పంటలతో (సోయాబీన్, గోధుమ) మార్చి సాగు చేయాలి.",
                "తెగులు వ్యాప్తిని తగ్గించడానికి పంట అవశేషాలను దున్నాలి.",
                "VT-R1 పెరుగుదల దశలో ఆకులపై శిలీంద్ర సంహారిణిని పిచికారీ చేయాలి."
            ],
            "organic_options": [
                "బాసిల్లస్ సబ్‌టిలిస్ జీవ శిలీంద్ర సంహారిణి.",
                "ట్రైకోడెర్మా ఆధారిత నేల మెరుగుదలు.",
                "కంపోస్ట్ టీ ఆకులపై పిచికారీ."
            ],
            "chemical_options": [
                "అజోక్సిస్ట్రోబిన్ (క్వాడ్రిస్) ఎకరాకు 200 మి.లీ.",
                "ప్రొపికొనజోల్ (టిల్ట్) సిఫార్సు చేసిన మోతాదులో.",
                "పైరాక్లోస్ట్రోబిన్ + మెట్కొనజోల్ మిశ్రమం."
            ],
            "prevention": [
                "బూడిద ఆకు మచ్చ నిరోధక సంకర రకాలను నాటాలి.",
                "నిరంతర మొక్కజొన్న సాగును నివారించాలి.",
                "సరైన మొక్కల మధ్య దూరాన్ని నిర్వహించాలి."
            ]
        }
    },
    "Corn_(maize)___Common_rust_": {
        "EN": {
            "disease_name": "Corn Common Rust",
            "crop": "Corn (Maize)",
            "cause": "Fungus Puccinia sorghi. Spores carried by wind from tropical regions.",
            "symptoms": [
                "Small, circular to elongate reddish-brown pustules on both leaf surfaces.",
                "Pustules break open releasing powdery rust spores.",
                "Heavily infected leaves may yellow and die."
            ],
            "treatment_steps": [
                "Scout fields regularly after tasseling.",
                "Apply foliar fungicide if pustules appear before tasseling.",
                "Remove severely infected plant debris after harvest."
            ],
            "organic_options": [
                "Neem oil spray as preventative.",
                "Sulfur-based organic fungicide.",
                "Encourage beneficial insects that feed on spores."
            ],
            "chemical_options": [
                "Mancozeb 75 WP (2.5g/L).",
                "Propiconazole at recommended dose.",
                "Azoxystrobin + Propiconazole combination."
            ],
            "prevention": [
                "Plant rust-resistant corn hybrids.",
                "Early planting to avoid peak spore season.",
                "Balanced nitrogen fertilization."
            ]
        },
        "HI": {
            "disease_name": "Corn Common Rust (हिंदी)",
            "crop": "मक्का",
            "cause": "Fungus Puccinia sorghi. Spores carried by wind from tropical regions.",
            "symptoms": [
                "Small, circular to elongate reddish-brown pustules on both leaf surfaces.",
                "Pustules break open releasing powdery rust spores.",
                "Heavily infected leaves may yellow and die."
            ],
            "treatment_steps": [
                "Scout fields regularly after tasseling.",
                "Apply foliar fungicide if pustules appear before tasseling.",
                "Remove severely infected plant debris after harvest."
            ],
            "organic_options": [
                "Neem oil spray as preventative.",
                "Sulfur-based organic fungicide.",
                "Encourage beneficial insects that feed on spores."
            ],
            "chemical_options": [
                "Mancozeb 75 WP (2.5g/L).",
                "Propiconazole at recommended dose.",
                "Azoxystrobin + Propiconazole combination."
            ],
            "prevention": [
                "Plant rust-resistant corn hybrids.",
                "Early planting to avoid peak spore season.",
                "Balanced nitrogen fertilization."
            ]
        },
        "TE": {
            "disease_name": "Corn Common Rust (తెలుగు)",
            "crop": "మొక్కజొన్న",
            "cause": "Fungus Puccinia sorghi. Spores carried by wind from tropical regions.",
            "symptoms": [
                "Small, circular to elongate reddish-brown pustules on both leaf surfaces.",
                "Pustules break open releasing powdery rust spores.",
                "Heavily infected leaves may yellow and die."
            ],
            "treatment_steps": [
                "Scout fields regularly after tasseling.",
                "Apply foliar fungicide if pustules appear before tasseling.",
                "Remove severely infected plant debris after harvest."
            ],
            "organic_options": [
                "Neem oil spray as preventative.",
                "Sulfur-based organic fungicide.",
                "Encourage beneficial insects that feed on spores."
            ],
            "chemical_options": [
                "Mancozeb 75 WP (2.5g/L).",
                "Propiconazole at recommended dose.",
                "Azoxystrobin + Propiconazole combination."
            ],
            "prevention": [
                "Plant rust-resistant corn hybrids.",
                "Early planting to avoid peak spore season.",
                "Balanced nitrogen fertilization."
            ]
        }
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "EN": {
            "disease_name": "Corn Northern Leaf Blight",
            "crop": "Corn (Maize)",
            "cause": "Fungus Exserohilum turcicum. Favors moderate temperatures (18-27°C) and high humidity.",
            "symptoms": [
                "Large, cigar-shaped gray-green to tan lesions (up to 15cm).",
                "Lesions start on lower leaves and progress upward.",
                "Severe infection causes significant yield loss."
            ],
            "treatment_steps": [
                "Apply fungicide at early tassel stage if disease is present.",
                "Rotate crops to break disease cycle.",
                "Incorporate infected residue into soil after harvest."
            ],
            "organic_options": [
                "Trichoderma harzianum soil application.",
                "Copper hydroxide spray.",
                "Crop rotation with legumes."
            ],
            "chemical_options": [
                "Azoxystrobin at recommended rate.",
                "Propiconazole + Azoxystrobin premix.",
                "Mancozeb 75 WP (2.5g/L)."
            ],
            "prevention": [
                "Select resistant hybrids (Ht genes).",
                "Avoid no-till continuous corn.",
                "Ensure adequate plant spacing for air flow."
            ]
        },
        "HI": {
            "disease_name": "Corn Northern Leaf Blight (हिंदी)",
            "crop": "मक्का",
            "cause": "Fungus Exserohilum turcicum. Favors moderate temperatures (18-27°C) and high humidity.",
            "symptoms": [
                "Large, cigar-shaped gray-green to tan lesions (up to 15cm).",
                "Lesions start on lower leaves and progress upward.",
                "Severe infection causes significant yield loss."
            ],
            "treatment_steps": [
                "Apply fungicide at early tassel stage if disease is present.",
                "Rotate crops to break disease cycle.",
                "Incorporate infected residue into soil after harvest."
            ],
            "organic_options": [
                "Trichoderma harzianum soil application.",
                "Copper hydroxide spray.",
                "Crop rotation with legumes."
            ],
            "chemical_options": [
                "Azoxystrobin at recommended rate.",
                "Propiconazole + Azoxystrobin premix.",
                "Mancozeb 75 WP (2.5g/L)."
            ],
            "prevention": [
                "Select resistant hybrids (Ht genes).",
                "Avoid no-till continuous corn.",
                "Ensure adequate plant spacing for air flow."
            ]
        },
        "TE": {
            "disease_name": "మొక్కజొన్న ఉత్తర ఆకుమచ్చ తెగులు",
            "crop": "మొక్కజొన్న",
            "cause": "Exserohilum turcicum అనే శిలీంధ్రం వల్ల వస్తుంది. మధ్యస్థ ఉష్ణోగ్రతలు (18-27°C) మరియు అధిక తేమ దీనికి అనుకూలం.",
            "symptoms": [
                "పెద్ద, సిగార్ ఆకారంలో బూడిద-ఆకుపచ్చ నుండి గోధుమ రంగు మచ్చలు (15 సెం.మీ వరకు).",
                "మచ్చలు కింది ఆకులపై ప్రారంభమై పైకి వ్యాపిస్తాయి.",
                "తీవ్రమైన సంక్రమణ గణనీయమైన దిగుబడి నష్టానికి కారణమవుతుంది."
            ],
            "treatment_steps": [
                "తెగులు ఉంటే ప్రారంభ కంకి దశలో శిలీంద్రనాశకాలు పిచికారీ చేయాలి.",
                "తెగులు చక్రం నివారించడానికి పంట మార్పిడి చేయాలి.",
                "కోత తర్వాత సోకిన అవశేషాలను మట్టిలో కలిపి దున్నాలి."
            ],
            "organic_options": [
                "ట్రైకోడెర్మా హర్జైనమ్ నేల అనువర్తనం.",
                "కాపర్ హైడ్రాక్సైడ్ పిచికారీ.",
                "పప్పుధాన్యాల పంటలతో పంట మార్పిడి."
            ],
            "chemical_options": [
                "సిఫార్సు చేయబడిన మోతాదులో అజాక్సిస్ట్రోబిన్.",
                "ప్రొపికోనజోల్ + అజాక్సిస్ట్రోబిన్ ప్రీమిక్స్.",
                "మ్యాంకోజెబ్ 75 WP (2.5గ్రా/లీ)."
            ],
            "prevention": [
                "నిరోధక హైబ్రిడ్‌లను (Ht జన్యువులు) ఎంచుకోండి.",
                "దున్నకుండా నిరంతర మొక్కజొన్న సాగును నివారించండి.",
                "గాలి ప్రసరణ కోసం మొక్కల మధ్య తగినంత దూరం ఉండేలా చూసుకోండి."
            ]
        }
    },
    "Grape___Black_rot": {
        "EN": {
            "disease_name": "Grape Black Rot",
            "crop": "Grape",
            "cause": "Fungus Guignardia bidwellii. Thrives in warm, humid weather during early growth.",
            "symptoms": [
                "Circular tan leaf spots with dark borders.",
                "Berries turn brown, shrivel into hard black mummies.",
                "Tendrils and shoots develop elongated cankers."
            ],
            "treatment_steps": [
                "Remove all mummified fruit and infected debris.",
                "Apply fungicide from bud break through veraison.",
                "Prune vines to improve air circulation."
            ],
            "organic_options": [
                "Copper-based fungicide early season.",
                "Sulfur dust during dry weather.",
                "Neem oil as supplemental spray."
            ],
            "chemical_options": [
                "Myclobutanil (Rally) at label rate.",
                "Captan 50 WP (2g/L).",
                "Mancozeb 75 WP before bloom."
            ],
            "prevention": [
                "Remove all mummies from vineyard floor.",
                "Open canopy for better drying.",
                "Plant resistant varieties when possible."
            ]
        },
        "HI": {
            "disease_name": "Grape Black Rot (हिंदी)",
            "crop": "अंगूर",
            "cause": "Fungus Guignardia bidwellii. Thrives in warm, humid weather during early growth.",
            "symptoms": [
                "Circular tan leaf spots with dark borders.",
                "Berries turn brown, shrivel into hard black mummies.",
                "Tendrils and shoots develop elongated cankers."
            ],
            "treatment_steps": [
                "Remove all mummified fruit and infected debris.",
                "Apply fungicide from bud break through veraison.",
                "Prune vines to improve air circulation."
            ],
            "organic_options": [
                "Copper-based fungicide early season.",
                "Sulfur dust during dry weather.",
                "Neem oil as supplemental spray."
            ],
            "chemical_options": [
                "Myclobutanil (Rally) at label rate.",
                "Captan 50 WP (2g/L).",
                "Mancozeb 75 WP before bloom."
            ],
            "prevention": [
                "Remove all mummies from vineyard floor.",
                "Open canopy for better drying.",
                "Plant resistant varieties when possible."
            ]
        },
        "TE": {
            "disease_name": "Grape Black Rot (తెలుగు)",
            "crop": "ద్రాక్ష",
            "cause": "Fungus Guignardia bidwellii. Thrives in warm, humid weather during early growth.",
            "symptoms": [
                "Circular tan leaf spots with dark borders.",
                "Berries turn brown, shrivel into hard black mummies.",
                "Tendrils and shoots develop elongated cankers."
            ],
            "treatment_steps": [
                "Remove all mummified fruit and infected debris.",
                "Apply fungicide from bud break through veraison.",
                "Prune vines to improve air circulation."
            ],
            "organic_options": [
                "Copper-based fungicide early season.",
                "Sulfur dust during dry weather.",
                "Neem oil as supplemental spray."
            ],
            "chemical_options": [
                "Myclobutanil (Rally) at label rate.",
                "Captan 50 WP (2g/L).",
                "Mancozeb 75 WP before bloom."
            ],
            "prevention": [
                "Remove all mummies from vineyard floor.",
                "Open canopy for better drying.",
                "Plant resistant varieties when possible."
            ]
        }
    },
    "Grape___Esca_(Black_Measles)": {
        "EN": {
            "disease_name": "Grape Esca (Black Measles)",
            "crop": "Grape",
            "cause": "Fungal complex: Phaeomoniella and Phaeoacremonium spp. Wood-inhabiting fungi.",
            "symptoms": [
                "Interveinal leaf striping and scorching.",
                "Dark spots on berries resembling measles.",
                "Sudden vine collapse (apoplexy) in severe cases."
            ],
            "treatment_steps": [
                "Prune during dry weather to minimize infection.",
                "Apply wound sealant to large pruning cuts.",
                "Remove and destroy severely infected vines."
            ],
            "organic_options": [
                "Trichoderma-based biocontrol on pruning wounds.",
                "Garlic extract foliar spray.",
                "Compost application to improve plant vigor."
            ],
            "chemical_options": [
                "Sodium arsenite (where legally permitted).",
                "Fosetyl-Al trunk injection.",
                "Thiophanate-methyl wound paint."
            ],
            "prevention": [
                "Avoid pruning in wet conditions.",
                "Use double pruning technique.",
                "Source planting material from certified nurseries."
            ]
        },
        "HI": {
            "disease_name": "Grape Esca (Black Measles) (हिंदी)",
            "crop": "अंगूर",
            "cause": "Fungal complex: Phaeomoniella and Phaeoacremonium spp. Wood-inhabiting fungi.",
            "symptoms": [
                "Interveinal leaf striping and scorching.",
                "Dark spots on berries resembling measles.",
                "Sudden vine collapse (apoplexy) in severe cases."
            ],
            "treatment_steps": [
                "Prune during dry weather to minimize infection.",
                "Apply wound sealant to large pruning cuts.",
                "Remove and destroy severely infected vines."
            ],
            "organic_options": [
                "Trichoderma-based biocontrol on pruning wounds.",
                "Garlic extract foliar spray.",
                "Compost application to improve plant vigor."
            ],
            "chemical_options": [
                "Sodium arsenite (where legally permitted).",
                "Fosetyl-Al trunk injection.",
                "Thiophanate-methyl wound paint."
            ],
            "prevention": [
                "Avoid pruning in wet conditions.",
                "Use double pruning technique.",
                "Source planting material from certified nurseries."
            ]
        },
        "TE": {
            "disease_name": "Grape Esca (Black Measles) (తెలుగు)",
            "crop": "ద్రాక్ష",
            "cause": "Fungal complex: Phaeomoniella and Phaeoacremonium spp. Wood-inhabiting fungi.",
            "symptoms": [
                "Interveinal leaf striping and scorching.",
                "Dark spots on berries resembling measles.",
                "Sudden vine collapse (apoplexy) in severe cases."
            ],
            "treatment_steps": [
                "Prune during dry weather to minimize infection.",
                "Apply wound sealant to large pruning cuts.",
                "Remove and destroy severely infected vines."
            ],
            "organic_options": [
                "Trichoderma-based biocontrol on pruning wounds.",
                "Garlic extract foliar spray.",
                "Compost application to improve plant vigor."
            ],
            "chemical_options": [
                "Sodium arsenite (where legally permitted).",
                "Fosetyl-Al trunk injection.",
                "Thiophanate-methyl wound paint."
            ],
            "prevention": [
                "Avoid pruning in wet conditions.",
                "Use double pruning technique.",
                "Source planting material from certified nurseries."
            ]
        }
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "EN": {
            "disease_name": "Grape Leaf Blight (Isariopsis)",
            "crop": "Grape",
            "cause": "Fungus Pseudocercospora vitis. Favors warm, humid monsoon conditions.",
            "symptoms": [
                "Dark brown irregular spots on leaf margins.",
                "Yellow halo around lesions.",
                "Premature defoliation reducing vine vigor."
            ],
            "treatment_steps": [
                "Remove fallen infected leaves from vineyard.",
                "Apply fungicide spray at disease onset.",
                "Ensure proper vine training for air flow."
            ],
            "organic_options": [
                "Bordeaux mixture (1%) spray.",
                "Neem oil at 5ml/L.",
                "Pseudomonas fluorescens biocontrol."
            ],
            "chemical_options": [
                "Mancozeb 75 WP (2.5g/L).",
                "Carbendazim 50 WP (1g/L).",
                "Copper oxychloride (3g/L)."
            ],
            "prevention": [
                "Avoid overhead irrigation.",
                "Maintain weed-free vineyard floor.",
                "Balanced fertilization to avoid excess nitrogen."
            ]
        },
        "HI": {
            "disease_name": "Grape Leaf Blight (Isariopsis) (हिंदी)",
            "crop": "अंगूर",
            "cause": "Fungus Pseudocercospora vitis. Favors warm, humid monsoon conditions.",
            "symptoms": [
                "Dark brown irregular spots on leaf margins.",
                "Yellow halo around lesions.",
                "Premature defoliation reducing vine vigor."
            ],
            "treatment_steps": [
                "Remove fallen infected leaves from vineyard.",
                "Apply fungicide spray at disease onset.",
                "Ensure proper vine training for air flow."
            ],
            "organic_options": [
                "Bordeaux mixture (1%) spray.",
                "Neem oil at 5ml/L.",
                "Pseudomonas fluorescens biocontrol."
            ],
            "chemical_options": [
                "Mancozeb 75 WP (2.5g/L).",
                "Carbendazim 50 WP (1g/L).",
                "Copper oxychloride (3g/L)."
            ],
            "prevention": [
                "Avoid overhead irrigation.",
                "Maintain weed-free vineyard floor.",
                "Balanced fertilization to avoid excess nitrogen."
            ]
        },
        "TE": {
            "disease_name": "Grape Leaf Blight (Isariopsis) (తెలుగు)",
            "crop": "ద్రాక్ష",
            "cause": "Fungus Pseudocercospora vitis. Favors warm, humid monsoon conditions.",
            "symptoms": [
                "Dark brown irregular spots on leaf margins.",
                "Yellow halo around lesions.",
                "Premature defoliation reducing vine vigor."
            ],
            "treatment_steps": [
                "Remove fallen infected leaves from vineyard.",
                "Apply fungicide spray at disease onset.",
                "Ensure proper vine training for air flow."
            ],
            "organic_options": [
                "Bordeaux mixture (1%) spray.",
                "Neem oil at 5ml/L.",
                "Pseudomonas fluorescens biocontrol."
            ],
            "chemical_options": [
                "Mancozeb 75 WP (2.5g/L).",
                "Carbendazim 50 WP (1g/L).",
                "Copper oxychloride (3g/L)."
            ],
            "prevention": [
                "Avoid overhead irrigation.",
                "Maintain weed-free vineyard floor.",
                "Balanced fertilization to avoid excess nitrogen."
            ]
        }
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "EN": {
            "disease_name": "Citrus Greening (Huanglongbing)",
            "crop": "Orange",
            "cause": "Bacterium Candidatus Liberibacter spp., transmitted by Asian citrus psyllid.",
            "symptoms": [
                "Asymmetric blotchy mottling of leaves.",
                "Small, lopsided, bitter fruit that stays green.",
                "Twig dieback and overall tree decline."
            ],
            "treatment_steps": [
                "Control psyllid vector with systemic insecticides.",
                "Remove and destroy confirmed infected trees.",
                "Apply nutritional sprays to maintain tree health."
            ],
            "organic_options": [
                "Kaolin clay spray to deter psyllids.",
                "Release Tamarixia radiata parasitoid wasps.",
                "Neem oil for psyllid suppression."
            ],
            "chemical_options": [
                "Imidacloprid soil drench for psyllid control.",
                "Dimethoate foliar spray.",
                "Spirotetramat (Movento) systemic."
            ],
            "prevention": [
                "Use disease-free certified nursery stock.",
                "Regular scouting for psyllid populations.",
                "Community-wide psyllid management programs."
            ]
        },
        "HI": {
            "disease_name": "Citrus Greening (Huanglongbing) (हिंदी)",
            "crop": "संतरा",
            "cause": "Bacterium Candidatus Liberibacter spp., transmitted by Asian citrus psyllid.",
            "symptoms": [
                "Asymmetric blotchy mottling of leaves.",
                "Small, lopsided, bitter fruit that stays green.",
                "Twig dieback and overall tree decline."
            ],
            "treatment_steps": [
                "Control psyllid vector with systemic insecticides.",
                "Remove and destroy confirmed infected trees.",
                "Apply nutritional sprays to maintain tree health."
            ],
            "organic_options": [
                "Kaolin clay spray to deter psyllids.",
                "Release Tamarixia radiata parasitoid wasps.",
                "Neem oil for psyllid suppression."
            ],
            "chemical_options": [
                "Imidacloprid soil drench for psyllid control.",
                "Dimethoate foliar spray.",
                "Spirotetramat (Movento) systemic."
            ],
            "prevention": [
                "Use disease-free certified nursery stock.",
                "Regular scouting for psyllid populations.",
                "Community-wide psyllid management programs."
            ]
        },
        "TE": {
            "disease_name": "Citrus Greening (Huanglongbing) (తెలుగు)",
            "crop": "నారింజ",
            "cause": "Bacterium Candidatus Liberibacter spp., transmitted by Asian citrus psyllid.",
            "symptoms": [
                "Asymmetric blotchy mottling of leaves.",
                "Small, lopsided, bitter fruit that stays green.",
                "Twig dieback and overall tree decline."
            ],
            "treatment_steps": [
                "Control psyllid vector with systemic insecticides.",
                "Remove and destroy confirmed infected trees.",
                "Apply nutritional sprays to maintain tree health."
            ],
            "organic_options": [
                "Kaolin clay spray to deter psyllids.",
                "Release Tamarixia radiata parasitoid wasps.",
                "Neem oil for psyllid suppression."
            ],
            "chemical_options": [
                "Imidacloprid soil drench for psyllid control.",
                "Dimethoate foliar spray.",
                "Spirotetramat (Movento) systemic."
            ],
            "prevention": [
                "Use disease-free certified nursery stock.",
                "Regular scouting for psyllid populations.",
                "Community-wide psyllid management programs."
            ]
        }
    },
    "Peach___Bacterial_spot": {
        "EN": {
            "disease_name": "Peach Bacterial Spot",
            "crop": "Peach",
            "cause": "Bacterium Xanthomonas arboricola pv. pruni. Spread by wind-driven rain.",
            "symptoms": [
                "Small, angular water-soaked leaf spots.",
                "Spots turn dark brown with yellow halos.",
                "Fruit develops sunken, cracked lesions."
            ],
            "treatment_steps": [
                "Apply copper sprays at petal fall.",
                "Remove severely infected branches.",
                "Avoid overhead irrigation to reduce splash spread."
            ],
            "organic_options": [
                "Copper hydroxide at reduced rates.",
                "Bacillus subtilis biological spray.",
                "Neem oil as supplemental spray."
            ],
            "chemical_options": [
                "Oxytetracycline (Mycoshield) at label rate.",
                "Copper + Mancozeb tank mix.",
                "Kasugamycin where registered."
            ],
            "prevention": [
                "Plant resistant cultivars.",
                "Proper tree spacing for air movement.",
                "Sanitary pruning of infected wood."
            ]
        },
        "HI": {
            "disease_name": "Peach Bacterial Spot (हिंदी)",
            "crop": "आड़ू",
            "cause": "Bacterium Xanthomonas arboricola pv. pruni. Spread by wind-driven rain.",
            "symptoms": [
                "Small, angular water-soaked leaf spots.",
                "Spots turn dark brown with yellow halos.",
                "Fruit develops sunken, cracked lesions."
            ],
            "treatment_steps": [
                "Apply copper sprays at petal fall.",
                "Remove severely infected branches.",
                "Avoid overhead irrigation to reduce splash spread."
            ],
            "organic_options": [
                "Copper hydroxide at reduced rates.",
                "Bacillus subtilis biological spray.",
                "Neem oil as supplemental spray."
            ],
            "chemical_options": [
                "Oxytetracycline (Mycoshield) at label rate.",
                "Copper + Mancozeb tank mix.",
                "Kasugamycin where registered."
            ],
            "prevention": [
                "Plant resistant cultivars.",
                "Proper tree spacing for air movement.",
                "Sanitary pruning of infected wood."
            ]
        },
        "TE": {
            "disease_name": "Peach Bacterial Spot (తెలుగు)",
            "crop": "పీచ్",
            "cause": "Bacterium Xanthomonas arboricola pv. pruni. Spread by wind-driven rain.",
            "symptoms": [
                "Small, angular water-soaked leaf spots.",
                "Spots turn dark brown with yellow halos.",
                "Fruit develops sunken, cracked lesions."
            ],
            "treatment_steps": [
                "Apply copper sprays at petal fall.",
                "Remove severely infected branches.",
                "Avoid overhead irrigation to reduce splash spread."
            ],
            "organic_options": [
                "Copper hydroxide at reduced rates.",
                "Bacillus subtilis biological spray.",
                "Neem oil as supplemental spray."
            ],
            "chemical_options": [
                "Oxytetracycline (Mycoshield) at label rate.",
                "Copper + Mancozeb tank mix.",
                "Kasugamycin where registered."
            ],
            "prevention": [
                "Plant resistant cultivars.",
                "Proper tree spacing for air movement.",
                "Sanitary pruning of infected wood."
            ]
        }
    },
    "Pepper,_bell___Bacterial_spot": {
        "EN": {
            "disease_name": "Pepper Bacterial Spot",
            "crop": "Pepper (Bell)",
            "cause": "Bacterium Xanthomonas campestris pv. vesicatoria. Seed-borne and rain-splashed.",
            "symptoms": [
                "Small, dark, water-soaked spots on leaves.",
                "Spots enlarge with yellow halos.",
                "Raised, scab-like lesions on fruit."
            ],
            "treatment_steps": [
                "Remove infected plant debris immediately.",
                "Apply copper-based bactericide at first symptoms.",
                "Use drip irrigation to avoid leaf wetness."
            ],
            "organic_options": [
                "Copper hydroxide spray (2g/L).",
                "Bacillus amyloliquefaciens biocontrol.",
                "Hot water seed treatment (50°C, 25 min)."
            ],
            "chemical_options": [
                "Copper oxychloride + Mancozeb.",
                "Streptomycin sulfate where permitted.",
                "Kasugamycin at recommended rates."
            ],
            "prevention": [
                "Use certified disease-free seed.",
                "Rotate with non-solanaceous crops (3-year).",
                "Avoid working in fields when foliage is wet."
            ]
        },
        "HI": {
            "disease_name": "Pepper Bacterial Spot (हिंदी)",
            "crop": "शिमला मिर्च",
            "cause": "Bacterium Xanthomonas campestris pv. vesicatoria. Seed-borne and rain-splashed.",
            "symptoms": [
                "Small, dark, water-soaked spots on leaves.",
                "Spots enlarge with yellow halos.",
                "Raised, scab-like lesions on fruit."
            ],
            "treatment_steps": [
                "Remove infected plant debris immediately.",
                "Apply copper-based bactericide at first symptoms.",
                "Use drip irrigation to avoid leaf wetness."
            ],
            "organic_options": [
                "Copper hydroxide spray (2g/L).",
                "Bacillus amyloliquefaciens biocontrol.",
                "Hot water seed treatment (50°C, 25 min)."
            ],
            "chemical_options": [
                "Copper oxychloride + Mancozeb.",
                "Streptomycin sulfate where permitted.",
                "Kasugamycin at recommended rates."
            ],
            "prevention": [
                "Use certified disease-free seed.",
                "Rotate with non-solanaceous crops (3-year).",
                "Avoid working in fields when foliage is wet."
            ]
        },
        "TE": {
            "disease_name": "Pepper Bacterial Spot (తెలుగు)",
            "crop": "క్యాప్సికమ్",
            "cause": "Bacterium Xanthomonas campestris pv. vesicatoria. Seed-borne and rain-splashed.",
            "symptoms": [
                "Small, dark, water-soaked spots on leaves.",
                "Spots enlarge with yellow halos.",
                "Raised, scab-like lesions on fruit."
            ],
            "treatment_steps": [
                "Remove infected plant debris immediately.",
                "Apply copper-based bactericide at first symptoms.",
                "Use drip irrigation to avoid leaf wetness."
            ],
            "organic_options": [
                "Copper hydroxide spray (2g/L).",
                "Bacillus amyloliquefaciens biocontrol.",
                "Hot water seed treatment (50°C, 25 min)."
            ],
            "chemical_options": [
                "Copper oxychloride + Mancozeb.",
                "Streptomycin sulfate where permitted.",
                "Kasugamycin at recommended rates."
            ],
            "prevention": [
                "Use certified disease-free seed.",
                "Rotate with non-solanaceous crops (3-year).",
                "Avoid working in fields when foliage is wet."
            ]
        }
    },
    "Potato___Early_blight": {
        "EN": {
            "disease_name": "Potato Early Blight",
            "crop": "Potato",
            "cause": "Fungus Alternaria solani. Favors warm days, cool nights, and alternating wet/dry periods.",
            "symptoms": [
                "Dark brown concentric ring spots (target-like) on lower leaves.",
                "Leaves yellow and drop prematurely.",
                "Tubers develop dark, sunken, dry lesions."
            ],
            "treatment_steps": [
                "Apply fungicide at first sign of lesions.",
                "Remove lower infected leaves.",
                "Harvest tubers when fully mature."
            ],
            "organic_options": [
                "Copper-based fungicide spray.",
                "Bacillus subtilis biological control.",
                "Compost tea foliar application."
            ],
            "chemical_options": [
                "Chlorothalonil (Bravo) at 7-day intervals.",
                "Mancozeb 75 WP (2.5g/L).",
                "Azoxystrobin at recommended rate."
            ],
            "prevention": [
                "Use certified seed potatoes.",
                "Rotate with non-solanaceous crops.",
                "Maintain adequate soil fertility and irrigation."
            ]
        },
        "HI": {
            "disease_name": "Potato Early Blight (हिंदी)",
            "crop": "आलू",
            "cause": "Fungus Alternaria solani. Favors warm days, cool nights, and alternating wet/dry periods.",
            "symptoms": [
                "Dark brown concentric ring spots (target-like) on lower leaves.",
                "Leaves yellow and drop prematurely.",
                "Tubers develop dark, sunken, dry lesions."
            ],
            "treatment_steps": [
                "Apply fungicide at first sign of lesions.",
                "Remove lower infected leaves.",
                "Harvest tubers when fully mature."
            ],
            "organic_options": [
                "Copper-based fungicide spray.",
                "Bacillus subtilis biological control.",
                "Compost tea foliar application."
            ],
            "chemical_options": [
                "Chlorothalonil (Bravo) at 7-day intervals.",
                "Mancozeb 75 WP (2.5g/L).",
                "Azoxystrobin at recommended rate."
            ],
            "prevention": [
                "Use certified seed potatoes.",
                "Rotate with non-solanaceous crops.",
                "Maintain adequate soil fertility and irrigation."
            ]
        },
        "TE": {
            "disease_name": "Potato Early Blight (తెలుగు)",
            "crop": "బంగాళాదుంప",
            "cause": "Fungus Alternaria solani. Favors warm days, cool nights, and alternating wet/dry periods.",
            "symptoms": [
                "Dark brown concentric ring spots (target-like) on lower leaves.",
                "Leaves yellow and drop prematurely.",
                "Tubers develop dark, sunken, dry lesions."
            ],
            "treatment_steps": [
                "Apply fungicide at first sign of lesions.",
                "Remove lower infected leaves.",
                "Harvest tubers when fully mature."
            ],
            "organic_options": [
                "Copper-based fungicide spray.",
                "Bacillus subtilis biological control.",
                "Compost tea foliar application."
            ],
            "chemical_options": [
                "Chlorothalonil (Bravo) at 7-day intervals.",
                "Mancozeb 75 WP (2.5g/L).",
                "Azoxystrobin at recommended rate."
            ],
            "prevention": [
                "Use certified seed potatoes.",
                "Rotate with non-solanaceous crops.",
                "Maintain adequate soil fertility and irrigation."
            ]
        }
    },
    "Potato___Late_blight": {
        "EN": {
            "disease_name": "Potato Late Blight",
            "crop": "Potato",
            "cause": "Oomycete Phytophthora infestans. Spreads rapidly in cool, wet weather.",
            "symptoms": [
                "Water-soaked, dark green to brown lesions on leaves.",
                "White fuzzy sporulation on leaf undersides.",
                "Tubers develop firm, reddish-brown granular rot."
            ],
            "treatment_steps": [
                "Apply protectant fungicide before disease onset.",
                "Destroy all infected plant material.",
                "Harvest early if epidemic threatens."
            ],
            "organic_options": [
                "Copper hydroxide spray at 5-7 day intervals.",
                "Bordeaux mixture (1%).",
                "Rapid hilling to protect tubers."
            ],
            "chemical_options": [
                "Metalaxyl + Mancozeb (Ridomil Gold MZ).",
                "Cymoxanil + Mancozeb.",
                "Dimethomorph at recommended rate."
            ],
            "prevention": [
                "Use resistant varieties.",
                "Destroy volunteer potato plants.",
                "Avoid overhead irrigation at night."
            ]
        },
        "HI": {
            "disease_name": "आलू का पछेती झुलसा",
            "crop": "आलू",
            "cause": "ऊमाइसेट फाइटोफ्थोरा इन्फेस्टन्स। ठंडे, नम मौसम में तेज़ी से फैलता है।",
            "symptoms": [
                "पत्तियों पर पानी से भीगे हुए, गहरे हरे से भूरे धब्बे।",
                "पत्तियों के निचले हिस्सों पर सफेद रूईदार बीजाणु बनते हैं।",
                "कंदों में कठोर, लाल-भूरे दानेदार सड़ांध विकसित होती है।"
            ],
            "treatment_steps": [
                "रोग लगने से पहले सुरक्षात्मक फफूंदनाशक लगाएं।",
                "सभी संक्रमित पौधों के अवशेष नष्ट करें।",
                "यदि महामारी का खतरा हो तो जल्दी कटाई करें।"
            ],
            "organic_options": [
                "5-7 दिन के अंतराल पर कॉपर हाइड्रॉक्साइड का छिड़काव।",
                "बोर्डो मिश्रण (1%)।",
                "कंदों की सुरक्षा के लिए तेज़ी से मिट्टी चढ़ाना।"
            ],
            "chemical_options": [
                "मेटालेक्सिल + मैंकोज़ेब (रिडोमिल गोल्ड एमजेड)।",
                "साइमोक्सानिल + मैंकोज़ेब।",
                "डाइमेथोमॉर्फ अनुशंसित दर पर।"
            ],
            "prevention": [
                "प्रतिरोधी किस्मों का उपयोग करें।",
                "स्वयं उगने वाले आलू के पौधों को नष्ट करें।",
                "रात में ऊपर से सिंचाई करने से बचें।"
            ]
        },
        "TE": {
            "disease_name": "బంగాళాదుంప ఆలస్యమైన తెగులు",
            "crop": "బంగాళాదుంప",
            "cause": "ఊమైసెట్ ఫైటోఫ్థోరా ఇన్ఫెస్టాన్స్. చల్లని, తడి వాతావరణంలో వేగంగా వ్యాపిస్తుంది.",
            "symptoms": [
                "ఆకులపై నీటితో తడిసిన, ముదురు ఆకుపచ్చ నుండి గోధుమ రంగు గాయాలు.",
                "ఆకు అడుగు భాగాలలో తెలుపు వెంట్రుకల వంటి బీజాంశ ఉత్పత్తి.",
                "దుంపలు గట్టి, ఎరుపు-గోధుమ రంగు గింజల వంటి కుళ్ళిపోవడాన్ని అభివృద్ధి చెందుతాయి."
            ],
            "treatment_steps": [
                "తెగులు ప్రారంభానికి ముందు రక్షణాత్మక శిలీంధ్ర నాశినిని వర్తించండి.",
                "సోకిన అన్ని మొక్క పదార్థాన్ని నాశనం చేయండి.",
                "అంటువ్యాధి బెదిరిస్తే ముందుగానే కోయండి."
            ],
            "organic_options": [
                "5-7 రోజుల వ్యవధిలో కాపర్ హైడ్రాక్సైడ్ స్ప్రే.",
                "బోర్డియక్స్ మిశ్రమం (1%).",
                "దుంపలను రక్షించడానికి వేగవంతమైన మట్టిని ఎగదోయడం."
            ],
            "chemical_options": [
                "మెటలాక్సిల్ + మాంకోజెబ్ (రిడోమిల్ గోల్డ్ MZ).",
                "సైమాక్సానిల్ + మాంకోజెబ్.",
                "సిఫార్సు చేయబడిన మోతాదు వద్ద డిమెథోమోర్ఫ్."
            ],
            "prevention": [
                "నిరోధక రకాలను ఉపయోగించండి.",
                "స్వచ్ఛందంగా పెరిగే బంగాళాదుంప మొక్కలను నాశనం చేయండి.",
                "రాత్రిపూట పై నుండి నీటిపారుదలని నివారించండి."
            ]
        }
    },
    "Squash___Powdery_mildew": {
        "EN": {
            "disease_name": "Squash Powdery Mildew",
            "crop": "Squash",
            "cause": "Fungi Podosphaera xanthii and Erysiphe cichoracearum. Warm, dry, shaded conditions.",
            "symptoms": [
                "White, talcum-like powder on upper leaf surfaces.",
                "Yellowish patches under white growth.",
                "Leaves become brown and brittle, premature defoliation."
            ],
            "treatment_steps": [
                "Remove severely infected leaves promptly.",
                "Apply fungicide at first sign of white patches.",
                "Increase sun exposure by thinning foliage."
            ],
            "organic_options": [
                "Potassium bicarbonate (3g/L + surfactant).",
                "Sulfur spray in dry conditions.",
                "Milk spray (40% solution)."
            ],
            "chemical_options": [
                "Myclobutanil at label rate.",
                "Trifloxystrobin preventive spray.",
                "Chlorothalonil at 7-10 day intervals."
            ],
            "prevention": [
                "Plant resistant squash varieties.",
                "Provide adequate spacing (1.5m).",
                "Avoid excessive nitrogen fertilization."
            ]
        },
        "HI": {
            "disease_name": "Squash Powdery Mildew (हिंदी)",
            "crop": "कद्दू",
            "cause": "Fungi Podosphaera xanthii and Erysiphe cichoracearum. Warm, dry, shaded conditions.",
            "symptoms": [
                "White, talcum-like powder on upper leaf surfaces.",
                "Yellowish patches under white growth.",
                "Leaves become brown and brittle, premature defoliation."
            ],
            "treatment_steps": [
                "Remove severely infected leaves promptly.",
                "Apply fungicide at first sign of white patches.",
                "Increase sun exposure by thinning foliage."
            ],
            "organic_options": [
                "Potassium bicarbonate (3g/L + surfactant).",
                "Sulfur spray in dry conditions.",
                "Milk spray (40% solution)."
            ],
            "chemical_options": [
                "Myclobutanil at label rate.",
                "Trifloxystrobin preventive spray.",
                "Chlorothalonil at 7-10 day intervals."
            ],
            "prevention": [
                "Plant resistant squash varieties.",
                "Provide adequate spacing (1.5m).",
                "Avoid excessive nitrogen fertilization."
            ]
        },
        "TE": {
            "disease_name": "Squash Powdery Mildew (తెలుగు)",
            "crop": "గుమ్మడి",
            "cause": "Fungi Podosphaera xanthii and Erysiphe cichoracearum. Warm, dry, shaded conditions.",
            "symptoms": [
                "White, talcum-like powder on upper leaf surfaces.",
                "Yellowish patches under white growth.",
                "Leaves become brown and brittle, premature defoliation."
            ],
            "treatment_steps": [
                "Remove severely infected leaves promptly.",
                "Apply fungicide at first sign of white patches.",
                "Increase sun exposure by thinning foliage."
            ],
            "organic_options": [
                "Potassium bicarbonate (3g/L + surfactant).",
                "Sulfur spray in dry conditions.",
                "Milk spray (40% solution)."
            ],
            "chemical_options": [
                "Myclobutanil at label rate.",
                "Trifloxystrobin preventive spray.",
                "Chlorothalonil at 7-10 day intervals."
            ],
            "prevention": [
                "Plant resistant squash varieties.",
                "Provide adequate spacing (1.5m).",
                "Avoid excessive nitrogen fertilization."
            ]
        }
    },
    "Strawberry___Leaf_scorch": {
        "EN": {
            "disease_name": "Strawberry Leaf Scorch",
            "crop": "Strawberry",
            "cause": "Fungus Diplocarpon earlianum. Spread by splashing rain in warm, humid weather.",
            "symptoms": [
                "Small, dark purple spots on upper leaf surface.",
                "Spots enlarge, areas between turn reddish-purple.",
                "Severe infection causes leaf drying and scorching."
            ],
            "treatment_steps": [
                "Remove old, infected leaves after harvest.",
                "Apply fungicide from bloom through harvest.",
                "Renovate beds by mowing and thinning."
            ],
            "organic_options": [
                "Copper-based spray at early bloom.",
                "Neem oil at 5ml/L.",
                "Remove runners to reduce canopy density."
            ],
            "chemical_options": [
                "Captan 50 WP (2g/L).",
                "Myclobutanil at recommended rate.",
                "Azoxystrobin at label rate."
            ],
            "prevention": [
                "Plant resistant cultivars.",
                "Use raised beds with drip irrigation.",
                "Proper plant spacing (30cm) for air flow."
            ]
        },
        "HI": {
            "disease_name": "स्ट्रॉबेरी पत्ती झुलसा रोग",
            "crop": "स्ट्रॉबेरी",
            "cause": "फंगस डिप्लोकार्पोन अर्लियानम। गर्म, आर्द्र मौसम में छींटों वाली बारिश द्वारा फैलता है।",
            "symptoms": [
                "पत्ती की ऊपरी सतह पर छोटे, गहरे बैंगनी धब्बे।",
                "धब्बे बड़े हो जाते हैं, उनके बीच के क्षेत्र लाल-बैंगनी हो जाते हैं।",
                "गंभीर संक्रमण पत्ती का सूखना और झुलसन का कारण बनता है।"
            ],
            "treatment_steps": [
                "कटाई के बाद पुरानी, संक्रमित पत्तियों को हटाएँ।",
                "फूल आने से कटाई तक फफूंदनाशक का प्रयोग करें।",
                "घास काटने और विरलन द्वारा क्यारियों का नवीनीकरण करें।"
            ],
            "organic_options": [
                "शुरुआती फूल आने पर तांबा-आधारित स्प्रे।",
                "5 मिलीलीटर/लीटर पर नीम का तेल।",
                "चंदवा घनत्व कम करने के लिए धावकों को हटाएँ।"
            ],
            "chemical_options": [
                "कैप्टन 50 डब्ल्यूपी (2 ग्राम/लीटर)।",
                "माइक्लोबुटानिल अनुशंसित दर पर।",
                "एज़ोक्सिस्ट्रोबिन लेबल दर पर।"
            ],
            "prevention": [
                "प्रतिरोधी किस्में लगाएँ।",
                "ड्रिप सिंचाई के साथ उठी हुई क्यारियां उपयोग करें।",
                "हवा के प्रवाह के लिए उचित पौधों की दूरी (30 सेमी)।"
            ]
        },
        "TE": {
            "disease_name": "స్ట్రాబెర్రీ ఆకు మాడిపోవడం",
            "crop": "స్ట్రాబెర్రీ",
            "cause": "డిప్లోకార్పాన్ ఎర్లియానం అనే శిలీంధ్రం. వెచ్చని, తేమతో కూడిన వాతావరణంలో చిమ్మిన వర్షం ద్వారా వ్యాపిస్తుంది.",
            "symptoms": [
                "ఆకు పై ఉపరితలంపై చిన్న, ముదురు ఊదా మచ్చలు.",
                "మచ్చలు పెద్దవి అవుతాయి, వాటి మధ్య ప్రాంతాలు ఎరుపు-ఊదా రంగులోకి మారుతాయి.",
                "తీవ్రమైన సంక్రమణ ఆకు ఎండిపోవడం మరియు మాడిపోవడానికి కారణమవుతుంది."
            ],
            "treatment_steps": [
                "కోత తర్వాత పాత, సోకిన ఆకులను తొలగించండి.",
                "పూత నుండి కోత వరకు శిలీంద్రనాశకాన్ని వర్తించండి.",
                "కత్తిరించడం మరియు పల్చబరచడం ద్వారా పాదులను పునరుద్ధరించండి."
            ],
            "organic_options": [
                "ప్రారంభ పూత వద్ద రాగి ఆధారిత పిచికారీ.",
                "5మి.లీ/లీటరు వద్ద వేప నూనె.",
                "పందిరి సాంద్రతను తగ్గించడానికి రన్నర్లను తొలగించండి."
            ],
            "chemical_options": [
                "కాప్టాన్ 50 డబ్ల్యూపీ (2గ్రా/లీటరు).",
                "సిఫార్సు చేయబడిన మోతాదు వద్ద మైక్లోబ్యూటానిల్.",
                "లేబుల్ మోతాదు వద్ద అజాక్సిస్ట్రోబిన్."
            ],
            "prevention": [
                "నిరోధక రకాలను నాటండి.",
                "బిందు సేద్యంతో ఎత్తైన పాదులను ఉపయోగించండి.",
                "గాలి ప్రవాహం కోసం సరైన మొక్కల దూరం (30సెం.మీ)."
            ]
        }
    },
    "Tomato___Leaf_Mold": {
        "EN": {
            "disease_name": "Tomato Leaf Mold",
            "crop": "Tomato",
            "cause": "Fungus Passalora fulva. Thrives in greenhouse/high humidity (>85%) conditions.",
            "symptoms": [
                "Pale green to yellow spots on upper leaf surface.",
                "Olive-green to brown velvety mold on leaf underside.",
                "Leaves curl, wither and drop; fruit rarely affected."
            ],
            "treatment_steps": [
                "Improve ventilation in greenhouses immediately.",
                "Remove infected lower leaves.",
                "Apply fungicide at first symptoms."
            ],
            "organic_options": [
                "Bacillus subtilis biocontrol spray.",
                "Potassium bicarbonate (3g/L).",
                "Improve greenhouse ventilation."
            ],
            "chemical_options": [
                "Chlorothalonil at 7-day intervals.",
                "Mancozeb 75 WP (2.5g/L).",
                "Difenoconazole at label rate."
            ],
            "prevention": [
                "Maintain RH below 85% with ventilation.",
                "Use resistant tomato varieties (Cf genes).",
                "Avoid overhead watering; use drip irrigation."
            ]
        },
        "HI": {
            "disease_name": "Tomato Leaf Mold (हिंदी)",
            "crop": "टमाटर",
            "cause": "Fungus Passalora fulva. Thrives in greenhouse/high humidity (>85%) conditions.",
            "symptoms": [
                "Pale green to yellow spots on upper leaf surface.",
                "Olive-green to brown velvety mold on leaf underside.",
                "Leaves curl, wither and drop; fruit rarely affected."
            ],
            "treatment_steps": [
                "Improve ventilation in greenhouses immediately.",
                "Remove infected lower leaves.",
                "Apply fungicide at first symptoms."
            ],
            "organic_options": [
                "Bacillus subtilis biocontrol spray.",
                "Potassium bicarbonate (3g/L).",
                "Improve greenhouse ventilation."
            ],
            "chemical_options": [
                "Chlorothalonil at 7-day intervals.",
                "Mancozeb 75 WP (2.5g/L).",
                "Difenoconazole at label rate."
            ],
            "prevention": [
                "Maintain RH below 85% with ventilation.",
                "Use resistant tomato varieties (Cf genes).",
                "Avoid overhead watering; use drip irrigation."
            ]
        },
        "TE": {
            "disease_name": "Tomato Leaf Mold (తెలుగు)",
            "crop": "టమాటా",
            "cause": "Fungus Passalora fulva. Thrives in greenhouse/high humidity (>85%) conditions.",
            "symptoms": [
                "Pale green to yellow spots on upper leaf surface.",
                "Olive-green to brown velvety mold on leaf underside.",
                "Leaves curl, wither and drop; fruit rarely affected."
            ],
            "treatment_steps": [
                "Improve ventilation in greenhouses immediately.",
                "Remove infected lower leaves.",
                "Apply fungicide at first symptoms."
            ],
            "organic_options": [
                "Bacillus subtilis biocontrol spray.",
                "Potassium bicarbonate (3g/L).",
                "Improve greenhouse ventilation."
            ],
            "chemical_options": [
                "Chlorothalonil at 7-day intervals.",
                "Mancozeb 75 WP (2.5g/L).",
                "Difenoconazole at label rate."
            ],
            "prevention": [
                "Maintain RH below 85% with ventilation.",
                "Use resistant tomato varieties (Cf genes).",
                "Avoid overhead watering; use drip irrigation."
            ]
        }
    },
    "Tomato___Septoria_leaf_spot": {
        "EN": {
            "disease_name": "Tomato Septoria Leaf Spot",
            "crop": "Tomato",
            "cause": "Fungus Septoria lycopersici. Favors warm (20-25°C), wet weather with splashing rain.",
            "symptoms": [
                "Many small circular spots (2-3mm) with dark borders and gray centers.",
                "Tiny black pycnidia visible in center of spots.",
                "Lower leaves affected first, progressing upward."
            ],
            "treatment_steps": [
                "Remove infected lower leaves promptly.",
                "Apply fungicide before rainy periods.",
                "Mulch around plants to prevent soil splash."
            ],
            "organic_options": [
                "Copper-based fungicide at first symptoms.",
                "Garlic extract spray.",
                "Bacillus amyloliquefaciens biocontrol."
            ],
            "chemical_options": [
                "Chlorothalonil (Bravo) every 7-10 days.",
                "Mancozeb 75 WP (2.5g/L).",
                "Azoxystrobin at recommended rate."
            ],
            "prevention": [
                "Rotate away from tomato for 2 years.",
                "Stake and prune for air circulation.",
                "Water at base; avoid wetting foliage."
            ]
        },
        "HI": {
            "disease_name": "टमाटर सेप्टोरिया पत्ती धब्बा",
            "crop": "टमाटर",
            "cause": "कवक सेप्टोरिया लाइकोपर्सिकी। गर्म (20-25°C), नम मौसम और बारिश के छीटों के साथ अनुकूल होती है।",
            "symptoms": [
                "कई छोटे गोलाकार धब्बे (2-3 मिमी) गहरे किनारों और भूरे केंद्रों के साथ।",
                "धब्बों के केंद्र में छोटे काले पिकनिडिया दिखाई देते हैं।",
                "निचली पत्तियां पहले प्रभावित होती हैं, जो ऊपर की ओर बढ़ती हैं।"
            ],
            "treatment_steps": [
                "संक्रमित निचली पत्तियों को तुरंत हटाएँ।",
                "बरसात के मौसम से पहले फफूंदनाशक का छिड़काव करें।",
                "मिट्टी के छीटों को रोकने के लिए पौधों के चारों ओर पलवार करें।"
            ],
            "organic_options": [
                "पहले लक्षणों पर तांबा-आधारित फफूंदनाशक।",
                "लहसुन अर्क का स्प्रे।",
                "बैसिलस एमाइलोलिक्वेफेसिएन्स जैव-नियंत्रण।"
            ],
            "chemical_options": [
                "क्लोरोथालोनिल (ब्रेवो) हर 7-10 दिन में।",
                "मैनकोजेब 75 डब्ल्यू.पी. (2.5 ग्राम/ली.)।",
                "अनुशंसित दर पर एज़ोक्सिस्ट्रोबिन।"
            ],
            "prevention": [
                "2 साल के लिए टमाटर से फसल चक्रण करें।",
                "हवा के संचार के लिए डंडे का सहारा दें और छँटाई करें।",
                "जड़ों में पानी दें; पत्तियों को गीला करने से बचें।"
            ]
        },
        "TE": {
            "disease_name": "Tomato Septoria Leaf Spot (తెలుగు)",
            "crop": "టమాటా",
            "cause": "Fungus Septoria lycopersici. Favors warm (20-25°C), wet weather with splashing rain.",
            "symptoms": [
                "Many small circular spots (2-3mm) with dark borders and gray centers.",
                "Tiny black pycnidia visible in center of spots.",
                "Lower leaves affected first, progressing upward."
            ],
            "treatment_steps": [
                "Remove infected lower leaves promptly.",
                "Apply fungicide before rainy periods.",
                "Mulch around plants to prevent soil splash."
            ],
            "organic_options": [
                "Copper-based fungicide at first symptoms.",
                "Garlic extract spray.",
                "Bacillus amyloliquefaciens biocontrol."
            ],
            "chemical_options": [
                "Chlorothalonil (Bravo) every 7-10 days.",
                "Mancozeb 75 WP (2.5g/L).",
                "Azoxystrobin at recommended rate."
            ],
            "prevention": [
                "Rotate away from tomato for 2 years.",
                "Stake and prune for air circulation.",
                "Water at base; avoid wetting foliage."
            ]
        }
    }
}

def get_remedy_for_disease(disease_name: str) -> dict:
    """
    Returns the remedy dictionary mapping (EN, HI, TE) for a given disease string.
    If exact match isn't found, falls back to Tomato___healthy or a default.
    """
    if disease_name in REMEDIES:
        return REMEDIES[disease_name]
    
    for d in REMEDIES.keys():
        if d.lower() in disease_name.lower():
            return REMEDIES[d]
            
    return REMEDIES.get("Tomato___healthy")
