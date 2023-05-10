import os
import sys
import openai
import time

# PLACE YOUR API KEY HERE
openai.api_key = " "
lang = ''


def ai(prompt):
    print('👉 soru')
    print(prompt)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", #gpt-4
        messages=[
            {"role": "system", "content": systemPrompt()},
            {"role": "user", "content": prompt},
        ],
    )
    result = completion.choices[0].message.content.strip()
    print('👉 cevap')
    print(result)
    print('')
    return result


def systemPrompt():
    return {
             'tr': "SEO friendly içerik üreten bir makale yazarısın.",
       # ",
        'en': 'You are an SEO expert answering machine. All of your answers are SEO optimized. You don\'t make a statement. When you can\'t answer, you just write "error".',
    }[lang]

def titlePrompt(topic):
    return {
        'en': 'Suggest a title about "XX".',
        'tr': '"XX" hakkında rakam kullanmayarak SEO uyumlu bir tane başlık öner.'
    }[lang].replace('XX', topic)

def titleContentPrompt(title):
    return {
        'en': 'Write a paragraph about "XX".',
        'tr': '"XX" konusunda anahtar kelimeleri kullanarak, içerikte öğrenilecek bilgilerin bulunduğu uzun detaylı SEO uyumlu spot yaz. 1 paragraf olsun.'
    }[lang].replace('XX', title)

def subtitlePrompt(title, subtitleCount):
    return {
        'en': 'Suggest YY subtopic titles about "XX".',
        'tr': 'XX hakkında YY tane SEO uyumlu altbaşlık öner.'
    }[lang].replace('XX', title).replace('YY', subtitleCount)

def subtitleContentPrompt(subtitle):
    return {
        'en': 'Write a blog post about "XX".',
        'tr': 'XX hakkında birkaç tane paragraf yaz.'
    }[lang].replace('XX', subtitle)

def toList(text):
    lines = [e.strip() for e in text.strip().split('\n') if e]
    return [e.split(' ', 1)[1] for e in lines]


if __name__ == '__main__':
    lang = sys.argv[1]
    topics = list(map(str.strip, sys.argv[2].split(',')))
    subtitleCount = sys.argv[3]
    for index, topic in enumerate(topics, start=1):
        title = ai(titlePrompt(topic))
        titleContent = ai(titleContentPrompt(title))
        subtitles = toList(ai(subtitlePrompt(title, subtitleCount)))
        subtitleContents = []
        for sub in subtitles:
            s = ai(subtitleContentPrompt(sub))
            subtitleContents.append(s.split('\n\n'))
        # SAVE
        with open(f'{index}.html', 'w') as f:
            f.write(f'<h1>{title}</h1>\n<p>\n{titleContent}\n</p>')
            for i in range(len(subtitles)):
                f.write(f'\n<h2>{subtitles[i]}</h2>')
                for paragraf in subtitleContents[i]:
                    f.write(f'\n<p>\n{paragraf}\n</p>\n')
            f.write('\n\n')
            print(f'💾 dosya kaydedildi')

