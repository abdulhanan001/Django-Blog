from django.shortcuts import render, HttpResponse, redirect
from .models import Post, BlogComment
from django.contrib import messages
from .templatetags import extras


# Create your views here.

def blogHome(request):
    allPosts = Post.objects.all()
    context = {'allPosts': allPosts}

    return render(request, 'blog/blogHome.html', context)


def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()  # getting first elemnt by using first
    post.views = post.views +1
    post.save()
    comments = BlogComment.objects.filter(post=post,parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None) #exculde ko not equal k liy use krty hn Django main
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys(): # keys are (sno) of comment and replay are values of keys
            replyDict[reply.parent.sno]= [reply]
            #print(reply.sno)
            #print(replyDict[reply.sno])
        else:
            replyDict[reply.parent.sno].append(reply)
    context = {'post': post, 'comments': comments,'user':request.user,'replyDict':replyDict}
    return render(request, 'blog/blogPost.html', context)


def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get("parentSno")
        if parentSno =="":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post,parent=parent)
            comment.save()
            messages.success(request, "Your replay has been posted successfully")

    return redirect(f"/blog/{post.slug}")
#redirect('/blog/{}'.format({post.slug}))