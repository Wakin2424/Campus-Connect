from django.shortcuts import render
import Auth.models as models
from django.utils import timezone

# Create your views here.
def createQuestionNotificationSave(user_id, question_id):
    """
    Initialize and save a notification to the database with question and user information.
    
    Args:
        user_id (int): The ID of the user
        question_id (int): The ID of the question
    
    Returns:
        Notifications: The created notification object, or None if creation fails
    """
    try:
        # Get the user object
        user = models.AuthCustomuser.objects.get(id=user_id)
        
        # Get the question object
        question = models.Qa.objects.get(qa_id=question_id)
        
        # Create and save the notification
        notification = models.Notifications.objects.create(
            user=user,
            message_type='question',
            message=f"just created a new question❓",
            is_read=False,
            created_at=timezone.now()
        )
        
        return notification
        
    except models.AuthCustomuser.DoesNotExist:
        print(f"User with ID {user_id} does not exist")
        return None
    except models.Qa.DoesNotExist:
        print(f"Question with ID {question_id} does not exist")
        return None
    except Exception as e:
        print(f"Error creating notification: {str(e)}")
        return None

def createAnswernotification(user_id, answer_id):
    """
    Initialize and save a notification to the database with answer and user information.
    
    Args:
        user_id (int): The ID of the user
        answer_id (int): The ID of the answer
    
    Returns:
        Notifications: The created notification object, or None if creation fails
    """
    try:
        # Get the user object
        user = models.AuthCustomuser.objects.get(id=user_id)
        
        # Get the answer object
        answer = models.Answers.objects.get(qa_id=answer_id)
        
        # Create and save the notification
        notification = models.Notifications.objects.create(
            user=user,
            message_type='question_answer',
            message=f"just created a new answer 🟰",
            is_read=False,
            created_at=timezone.now()
        )
        
        return notification
        
    except models.AuthCustomuser.DoesNotExist:
        print(f"User with ID {user_id} does not exist")
        return None
    except models.Answers.DoesNotExist:
        print(f"Answer with ID {answer_id} does not exist")
        return None
    except Exception as e:
        print(f"Error creating notification: {str(e)}")
        return None

def createNoteNotification(user_id, note_id):
    """
    Initialize and save a notification to the database with note and user information.
    
    Args:
        user_id (int): The ID of the user
        note_id (int): The ID of the note
    
    Returns:
        Notifications: The created notification object, or None if creation fails
    """
    try:
        # Get the user object
        user = models.AuthCustomuser.objects.get(id=user_id)
        
        # Get the note object
        note = models.Notes.objects.get(qa_id=note_id)
        
        # Create and save the notification
        notification = models.Notifications.objects.create(
            user=user,
            message_type='question_note',
            message=f"just created a new note: {note.title}📝",
            is_read=False,
            created_at=timezone.now()
        )
        
        return notification
        
    except models.AuthCustomuser.DoesNotExist:
        print(f"User with ID {user_id} does not exist")
        return None
    except models.Notes.DoesNotExist:
        print(f"Note with ID {note_id} does not exist")
        return None
    except Exception as e:
        print(f"Error creating notification: {str(e)}")
        return None

def createGroupNotification(user_id, group_id):
    """
    Initialize and save a notification to the database with group and user information.
    
    Args:
        user_id (int): The ID of the user
        group_id (int): The ID of the group
    
    Returns:
        Notifications: The created notification object, or None if creation fails
    """
    try:
        # Get the user object
        user = models.AuthCustomuser.objects.get(id=user_id)
        
        # Get the group object
        group = models.Group.objects.get(qa_id=group_id)
        
        # Create and save the notification
        notification = models.Notifications.objects.create(
            user=user,
            message_type='group',
            message=f"just created a new group: {group.name}👥",
            is_read=False,
            created_at=timezone.now()
        )
        
        return notification
        
    except models.AuthCustomuser.DoesNotExist:
        print(f"User with ID {user_id} does not exist")
        return None
    except models.Groups.DoesNotExist:
        print(f"Group with ID {group_id} does not exist")
        return None
    except Exception as e:
        print(f"Error creating notification: {str(e)}")
        return None