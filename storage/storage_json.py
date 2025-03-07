import json
class Storage:
    def __init__(self, data):
        self.data = data


    def get_posts(self):

        """Gets all posts from the database"""

        try:
            with open(self.data, 'r') as file:
                return json.loads(file.read())
        except FileNotFoundError:
            print('Can not access the database!')
        except json.decoder.JSONDecodeError:
            print('Database is empty!')
        except Exception as e:
            print(f'The following error has occurred: {e}')


    def get_post_by_id(self, blog_posts, post_id):

        """Gets the particular post from the database by id"""

        for post in blog_posts:
            if post['id'] == post_id:
                return post



    def rewrite_posts(self, blog_posts):

        """Rewrites all the data in the database"""

        try:
            with open(self.data, 'w') as file:
                file.write(json.dumps(blog_posts))
        except FileNotFoundError:
            print('Can not access the database!')
        except json.decoder.JSONDecodeError:
            print('Database is empty!')
        except Exception as e:
            print(f'The following error has occurred: {e}')


    def add_post(self, blog_posts, author, title, content):

        """Appends post to the database"""

        post_id = 0
        if len(blog_posts) > 0:
            last_post_id = blog_posts[-1]['id']
            post_id = last_post_id
        new_post = {
            'id': post_id + 1,
            'author': author,
            'title': title,
            'content': content,
            'likes': 0,
            'is_liked': False
        }
        blog_posts.append(new_post)
        self.rewrite_posts(blog_posts)


    def delete_post(self, blog_posts, post_id):

        """Removes post from the database"""

        for post in blog_posts:
            if post['id'] == post_id:
                blog_posts.remove(post)
        self.rewrite_posts(blog_posts)


    def update_post(self, blog_posts, post_id, author, title, content):

        """Rewrites the particular post in the database"""

        for post in blog_posts:
            if post['id'] == post_id:
                post_index = blog_posts.index(post)
                blog_posts[post_index] = {
                    'id': post_id,
                    'author': author,
                    'title': title,
                    'content': content,
                    'likes': post['likes'],
                    'is_liked': post['is_liked']
                }
        self.rewrite_posts(blog_posts)


    def like_post(self, blog_posts, post_id):

        """
        If like button is not pressed, increases the likes amount in the database.
        If like button is pressed, decreases the likes amount in the database.
        """

        post = self.get_post_by_id(blog_posts, post_id)
        if not post['is_liked']:
            post['likes'] += 1
            post['is_liked'] = True
        else:
            post['likes'] -= 1
            post['is_liked'] = False
        self.rewrite_posts(blog_posts)
