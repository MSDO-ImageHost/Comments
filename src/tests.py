import unittest
import json
from dbmanager import get_all_comments, request_comment, update_comment, delete_comment, request_comments_for_post, create_comment, remove_all_comments
from receiver import session, send

class TestComments(unittest.TestCase):
    # Tests for dbmanager class
    test_auth_id = 2147483646
    test_post_id = 2147483645
    test_role = 6
    admin_role = 21

    def test_create_a_comment(self):
        loadedJson = json.loads(create_comment(session, self.test_auth_id, self.test_post_id, "This is a test"))
        httpResponse = loadedJson['http_response']

        # Clean database from test comment entry
        delete_comment(session, self.test_auth_id, loadedJson['comment_id'], self.admin_role)

        self.assertEqual(httpResponse, 200, "[-] Error creating comment")
    
    def test_request_comment_by_id(self):
        createJson = json.loads(create_comment(session, self.test_auth_id, self.test_post_id, "This is a test"))
        temp = request_comment(session, createJson['comment_id'])
        loadedJson = json.loads(temp)
        httpResponse = loadedJson['http_response']

        # Clean database from test comment entry
        delete_comment(session, self.test_auth_id, createJson['comment_id'], self.admin_role)

        self.assertEqual(httpResponse, 200, "[-] Error requesting comment")

    def test_request_comment_by_id_wrongId(self):
        createJson = json.loads(create_comment(session, self.test_auth_id, self.test_post_id, "This is a test"))
        temp = request_comment(session, self.test_auth_id)
        loadedJson = json.loads(temp)
        httpResponse = loadedJson['http_response']

        # Clean database from test comment entry
        delete_comment(session, self.test_auth_id, createJson['comment_id'], self.admin_role)

        self.assertEqual(httpResponse, 403, "[-] Requests with wrong ID, positive HTTP response anyways.")

    def test_update_comment_content(self):
        #createJson = json.loads(create_comment(session, 999999, 999999, "This is a test"))
        createJson = json.loads(create_comment(session, self.test_auth_id, self.test_post_id, "This is a test"))
        temp = update_comment(session, createJson['comment_id'], self.test_auth_id, "Rewrote test content", self.test_role)
        loadedJson = json.loads(temp)
        httpResponse = loadedJson['http_response']

        # Clean database from test comment entry
        delete_comment(session, self.test_auth_id, createJson['comment_id'], self.admin_role)

        self.assertEqual(httpResponse, 200, "[-] Error changing comment")

    def test_update_comment_wrong_author(self):
        createJson = json.loads(create_comment(session, self.test_auth_id, self.test_post_id, "This is a test"))
        temp = update_comment(session, createJson['comment_id'], 42, "Rewrote test content", self.test_role)
        loadedJson = json.loads(temp)
        httpResponse = loadedJson['http_response']

        # Clean database from test comment entry
        delete_comment(session, self.test_auth_id, createJson['comment_id'], self.admin_role)

        self.assertEqual(httpResponse, 403, "[-] Changing comment with wrong author still gives positive HTTP response.")

    def test_delete_a_comment(self):
        createJson = json.loads(create_comment(session, self.test_auth_id, self.test_post_id, "This is a test"))
        temp = delete_comment(session, self.test_auth_id, createJson['comment_id'], self.test_role)
        loadedJson = json.loads(temp)
        httpResponse = loadedJson['http_response']

        self.assertEqual(httpResponse, 200, "[-] Error deleting comment")

    def test_delete_a_comment_wrong_author(self):
        createJson = json.loads(create_comment(session, self.test_auth_id, self.test_post_id, "This is a test"))
        temp = delete_comment(session, 42, createJson['comment_id'], self.test_role)
        loadedJson = json.loads(temp)
        httpResponse = loadedJson['http_response']

        # Clean database from test comment entry
        delete_comment(session, self.test_auth_id, createJson['comment_id'], self.admin_role)

        self.assertEqual(httpResponse, 403, "[-] Deleting a comment with wrong author, still gives positive HTTP response.")



    # RabbitMQ tests

    # Send an event
    # Look in the database if the event has triggered anything
    


if __name__ == '__main__':
    unittest.main()