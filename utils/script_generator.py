from openai import OpenAI
import re

def generate_script(topic, video_type, duration, language, api_key=None):
    """
    Generates a script using an LLM.
    If no API key is provided, it returns a mock script scaled precisely to the duration.
    """
    if not api_key:
        # Mock logic to match requested duration without hitting API limits
        
        # We provide a few hardcoded mock sentences to demonstrate the language feature
        # without requiring the OpenAI API Key.
        if language == "Spanish":
            base_sentences = [
                f"Bienvenidos a este video {video_type.lower()} sobre {topic}.",
                f"Hoy vamos a profundizar en cómo {topic} impacta nuestras vidas.",
                f"Muchos expertos creen que entender {topic} es esencial.",
                f"Vamos a explorar los mecanismos centrales de cómo funciona.",
                f"Históricamente, el desarrollo en esta área fue lento.",
                f"Pero los avances recientes lo cambiaron todo.",
                f"Las aplicaciones de {topic} son amplias y abarcan múltiples industrias.",
                f"Desde mejorar la eficiencia hasta resolver problemas complejos.",
                f"Sin embargo, todavía hay desafíos que superar.",
                f"Esperamos ver aún más innovación en los próximos años.",
                f"Gracias por ver este resumen completo.",
                f"No olviden suscribirse para más contenido sobre {topic}."
            ]
        elif language == "French":
            base_sentences = [
                f"Bienvenue dans cette vidéo {video_type.lower()} sur {topic}.",
                f"Aujourd'hui, nous allons plonger au cœur de {topic}.",
                f"De nombreux experts pensent que comprendre {topic} est essentiel.",
                f"Explorons les mécanismes fondamentaux de son fonctionnement.",
                f"Historiquement, le développement dans ce domaine était lent.",
                f"Mais de récentes percées ont tout changé.",
                f"Les applications de {topic} sont vastes.",
                f"De l'amélioration de l'efficacité à la résolution de problèmes.",
                f"Cependant, il reste des défis à surmonter.",
                f"Nous nous attendons à encore plus d'innovation à l'avenir.",
                f"Merci d'avoir regardé cet aperçu complet.",
                f"N'oubliez pas de vous abonner pour plus de contenu sur {topic}."
            ]
        elif language == "Hindi":
            base_sentences = [
                f"{topic} के बारे में इस {video_type.lower()} वीडियो में आपका स्वागत है।",
                f"आज हम गहराई से जानेंगे कि {topic} हमारे जीवन को कैसे प्रभावित करता है।",
                f"कई विशेषज्ञों का मानना है कि {topic} को समझना आवश्यक है।",
                f"आइए जानें कि यह वास्तव में कैसे काम करता है।",
                f"ऐतिहासिक रूप से, इस क्षेत्र में विकास धीमा था।",
                f"लेकिन हाल की सफलताओं ने सब कुछ बदल दिया।",
                f"दक्षता में सुधार से लेकर जटिल समस्याओं को हल करने तक।",
                f"हालाँकि, अभी भी कुछ चुनौतियाँ हैं।",
                f"आने वाले वर्षों में, हम और भी अधिक नवाचार देखने की उम्मीद करते हैं।",
                f"इस अवलोकन को देखने के लिए धन्यवाद।",
                f"{topic} पर अधिक सामग्री के लिए सब्सक्राइब करना न भूलें।"
            ]
        elif language == "German":
            base_sentences = [
                f"Willkommen zu diesem {video_type.lower()} Video über {topic}.",
                f"Heute werden wir tief in {topic} eintauchen.",
                f"Viele Experten glauben, dass das Verständnis von {topic} wichtig ist.",
                f"Lassen Sie uns die Kernmechanismen erforschen.",
                f"Historisch gesehen war die Entwicklung in diesem Bereich langsam.",
                f"Aber jüngste Durchbrüche haben alles verändert.",
                f"Die Anwendungen von {topic} sind vielfältig.",
                f"Von der Verbesserung der Effizienz bis zur Problemlösung.",
                f"Es gibt jedoch noch Herausforderungen.",
                f"Wir erwarten in den kommenden Jahren noch mehr Innovationen.",
                f"Vielen Dank fürs Zuschauen.",
                f"Vergessen Sie nicht, für mehr Inhalte über {topic} zu abonnieren."
            ]
        else:
            base_sentences = [
                f"Welcome to this {video_type.lower()} video about {topic}.",
                f"Today, we are going to dive deep into how {topic} impacts our daily lives.",
                f"Many experts believe that understanding {topic} is essential for the future.",
                f"Let's explore the core mechanics of how it actually works.",
                f"Historically, development in this area was slow, but recent breakthroughs changed everything.",
                f"The applications of {topic} are vast and span across multiple industries.",
                f"From improving efficiency to solving complex problems, the benefits are clear.",
                f"However, there are still challenges that researchers are trying to overcome.",
                f"In the coming years, we expect to see even more innovation surrounding {topic}.",
                f"Moreover, the global community is investing heavily in advancing {topic}.",
                f"If we look at the data, the growth trajectory is absolutely staggering.",
                f"This brings us to a crucial question about the sustainability of {topic}.",
                f"Let's consider a practical example to illustrate this point clearly.",
                f"As you can see, the real-world implications are profound and far-reaching.",
                f"Industry leaders are already adopting these strategies to stay ahead.",
                f"But what does this mean for the average person?",
                f"It means that adapting to {topic} is no longer optional, it is mandatory.",
                f"Education and awareness will play a pivotal role in this transition.",
                f"We must remain vigilant and proactive in our approach.",
                f"Thank you for watching this comprehensive overview.",
                f"Don't forget to like and subscribe for more content on {topic}!"
            ]
            
        # Calculate target words (average 160 words per minute for clear AI dictation)
        if "1" in duration:
            target_words = 160 * 1
        elif "3" in duration:
            target_words = 160 * 3
        elif "5" in duration:
            target_words = 160 * 5
        else:
            target_words = 160
            
        script_sentences = []
        word_count = 0
        idx = 0
        
        # Loop through the base sentences until we hit the EXACT required word count for the duration
        while word_count < target_words:
            sentence = base_sentences[idx % len(base_sentences)]
            script_sentences.append(sentence)
            word_count += len(sentence.split())
            idx += 1
            
        return " ".join(script_sentences)
        
    client = OpenAI(api_key=api_key)
    prompt = (f"Write a detailed {video_type} video script about {topic} in the {language} language. "
              f"The video should be approximately {duration} long. "
              "Do not include camera instructions or visual cues, just provide the spoken text.")
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def split_into_scenes(script):
    """
    Splits the generated script into logical scenes.
    Groups sentences together to reduce image API calls and improve visual pacing.
    Supports English/European punctuation (.!?) and Hindi punctuation (।).
    """
    # Use regex to split by common sentence-ending punctuation including the Hindi Purna Viram (।)
    sentences = re.split(r'(?<=[.!?।])\s+', script.strip())
    
    scenes = []
    current_scene_sentences = []
    scene_count = 1
    
    for s in sentences:
        if s.strip():
            current_scene_sentences.append(s.strip())
            # Group 3 sentences per scene to show an image for ~10-15 seconds
            if len(current_scene_sentences) >= 3:
                scenes.append({
                    "scene_num": scene_count,
                    "text": " ".join(current_scene_sentences)
                })
                scene_count += 1
                current_scene_sentences = []
                
    # Add any remaining sentences as the last scene
    if current_scene_sentences:
        scenes.append({
            "scene_num": scene_count,
            "text": " ".join(current_scene_sentences)
        })
        
    return scenes