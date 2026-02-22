from django.shortcuts import render
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.conf import settings
from google import genai
import uuid

AI_model = genai.Client(api_key=settings.GOOGLE_API_KEY)

# Create your views here.
def saveAIanswer(question, answer):
    from Auth import models as Models
    user = Models.AuthCustomuser.objects.get(username='ModuloAI')
    answer = Models.Answers.objects.create(user=user, question=question, answer=answer, ai=True,code=uuid.uuid4())
    answer.save()

def AIanswer(request, id):
    from Auth import models as Models
    if request.method == 'POST':
        question = get_object_or_404(Models.Qa, code=id)

        prompt = f"""
            Answer the following question: {question.question}
            Description: {question.description}
            provide the answer in form of html text that is to be inserted in a html div element. If the question contains code, provide the answer in a code block with the appropriate language tag for syntax highlighting. If the question is asking for steps or a process, provide the answer in an ordered list format. If the question is asking for multiple solutions or methods, provide the answer in an unordered list format. Always ensure that the answer is clear, concise, and directly addresses the question asked.
        """
        try:
            response = AI_model.models.generate_content(
                model='gemini-3-flash-preview',
                contents=prompt,
            )

            saveAIanswer(question, response.text)
        except Exception as e:
            print(e)
            return JsonResponse({'status':False})

        context = {
            'status':True,
            'answer':response.text
        }
        
        return JsonResponse(context)
    return JsonResponse({'status':False})

def aiGroupChat(chat_history, new_message):
    prompt = f"""
        You are a helpful assistant for a group chat. The following is the chat history:
        {chat_history}
        A new message directed to you has been sent in the group chat: {new_message}
        Please provide a helpful and relevant response to the new message, taking into account the context of the previous messages in the chat history and keep it short and concise.
    """
    try:
        response = AI_model.models.generate_content(
            model='gemini-3-flash-preview',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(e)
        return None