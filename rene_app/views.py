from django.shortcuts import render, redirect
from .models import User, Question, Solution
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    context = {
        'allUsers': User.objects.all()
    }
    return render(request, "index.html", context)

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.my_validator(request.POST)
    c = User.objects.last()
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        c.delete()
        return redirect ('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash,
        )
        request.session['user_id'] = new_user.id
        return redirect('/home')

def login(request):
    if request.method == "GET":
        return redirect('/')
    user = User.objects.filter(email = request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['login_pw'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            print('id is', logged_user.id)
            return redirect('/home')
        else:
            messages.error(request, "Incorrect email or password")
        return redirect('/')
    messages.error(request, "No account with that information...please register")
    return redirect('/')   

def home(request):
    if 'user_id' not in request.session:
        print("not in session")
        return redirect('/')
    user = User.objects.get(id = request.session['user_id'])
    my_qs = Question.objects.filter(uploaded_by=user)
    all_qs = Question.objects.all()
    context = {
        'user': user,
        'questions': my_qs,
        'all_questions': all_qs
    }
    request.session['email'] = user.email
    return render(request, "userhome.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')

def post(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id = request.session['user_id'])
    if len(request.POST['description']) > 4:
        new_question = Question.objects.create(topics = request.POST['topic'], description=request.POST['description'], uploaded_by=user)
    return redirect(f'/question/{new_question.id}')

def question(request, q_id):
    if 'user_id' not in request.session:
        return redirect('/')
    # print('also check', Question.objects.all())
    this_q = Question.objects.get(id=q_id)
    this_user = User.objects.get(id=request.session['user_id'])
    this_solution = Solution.objects.filter(solution_for=this_q)
    context = {
        'this_question': this_q,
        'this_user': this_user,
        'this_solution': this_solution
    }
    return render(request, 'question.html', context)

def attempts(request, q_id):
    if 'user_id' not in request.session:
        print("not in session")
        return redirect('/')
    this_question = Question.objects.get(id=q_id)
    if len(request.POST['attempt']) > 4:
        new_solution = Solution.objects.create(attempt = request.POST['attempt'], resource=request.POST['resource'], solution_for=this_question)
        print('checking', new_solution)
    return redirect(f'/question/{this_question.id}')

def solutions(request, sol_id):
    if 'user_id' not in request.session:
        return redirect('/')
    this_solution = Solution.objects.get(id=sol_id)
    this_user = User.objects.get(id=request.session['user_id'])
    context = {
        'this_solution': this_solution,
        'this_user': this_user
    }
    return render(request, 'solution.html', context)
    
def comm_posts(request):
    x = Question.objects.filter(is_solved=True)
    y =Question.objects.filter(is_solved=False)
    context = {
        'solved': x,
        'unsolved':y
    }
    return render(request, 'community.html', context)

def agree(request, sol_id):
    c = Solution.objects.get(id=sol_id)
    c.agrees+=1
    if (c.agrees >= 3):
        c.solution = True
        x = c.solution_for.id
        y = Question.objects.get(id=x)
        y.is_solved = True
        y.save()
        c.save()
        return redirect(f'/question/{c.solution_for.id}')
    c.save()
    # print('check', c.id)
    return redirect(f'/question/{c.solution_for.id}')

def refute(request, sol_id):
    c = Solution.objects.get(id=sol_id)
    c.agrees-=1
    if (c.agrees < -2):
        c.delete()
        return redirect(f'/question/{c.solution_for.id}')
    if (c.agrees < 3):
        c.solution = False
        x = c.solution_for.id
        y = Question.objects.get(id=x)
        y.is_solved = False
        y.save()
        c.save()
        return redirect(f'/question/{c.solution_for.id}')
    c.save()
    return redirect(f'/question/{c.solution_for.id}')

def about(request):
    return render(request, 'about.html')

def resources (request):
    solved_ques = Question.objects.filter(is_solved = True)
    if (solved_ques):
        arr = []
        print('check', solved_ques)
        for solved in solved_ques:
            x = Solution.objects.filter(solution_for=solved)
            print('and here', len(x))
            # arr.append(x)
            y = len(x)
            print('array', x)
            while (y > 0):
                print('length', x[y-1].resource)
                arr.append(x[y-1].resource)
                y-=1
        context = {
            'solved': solved_ques,
            'solutions': arr
        }
        print('end', arr)
    return render(request, 'resources.html',context)