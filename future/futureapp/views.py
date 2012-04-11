# Create your views here.

# make a post.  first prototype.
def post(request):
    if request.method == 'POST':
        newPost = UserPost(title = 'foo', #title=request.POST['title'],
                     text = request.POST['text'],
                     author = request.session['userid'],
                     tags = (),
                     mentions = ())
        newPost.save()
        return HttpResponse('woot.')
    else:
        return HttpResponse('SOMETHING IS WRONG.')

        


