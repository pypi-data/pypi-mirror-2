.. _ref-index:

Welcome to milkman's documentation
==================================

``milkman`` is an open source fixture replacement for Django testing.

Instead of maintaining scores of fixtures, whether they be generated, dumped, or
managed semi-dynamically, it can still generate a lot of code that is not even
test code.  Furthermore, this tends to be brittle and hard to maintain.

The genius of ``milkman`` is that it randomly generates data for all the fields
on a particular object, while at the same time allowing the test writer to
override any particular field with their own data when determinate fields are
needed for a test.

Example::

    from django.contrib.auth.models import User
    from django.core.urlresolvers import reverse
    from django.test import TestCase, Client

    from milkman import milkman

    from app.models import Library, Book, Author


    class LibraryTest(TestCase):
    
        def setUp(self):
            self.user = milkman.deliver(User)
            self.user.set_password("letmein")
            self.user.save()
        
            self.user2 = milkman.deliver(User)
            self.user2.set_password("letmein")
            self.user2.save()
        
            self.library = milkman.deliver(Library)
            self.book = milkman.deliver(Book)
            self.author = milkman.deliver(Author, lastname="Lewis")
        
            self.client = Client()
            self.client.login(username=self.user.username, password="letmein")
        
            self.url = reverse("book", args=[self.library.id, self.book.id])

        def tearDown(self):
            self.user.delete()
            self.user2.delete()
            self.library.delete()
            self.book.delete()
            self.author.delete()

