import unittest
import os
from datetime import datetime
import shutil

from git_deployer.configutils import load_config
from git_deployer.gitdeploy import git_deploy
from git_deployer.gitutils import is_git_repo, is_bare_git_repo

class TestGitDeploy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        test_dir = os.path.dirname(os.path.realpath(__file__))
        cls.test_dir = test_dir
        test_config_path = os.path.join(test_dir, 'deploy_config.yml')
        cls.test_config_path = test_config_path
        print('\ntest config path:', test_config_path)
        config = load_config(config_path=test_config_path)
        cls.config = config
        test_repo_dir = os.path.join(test_dir, '.test_repo')
        print('test deploy repo path:', test_repo_dir)
        os.makedirs(test_repo_dir, exist_ok=True)
        if not is_bare_git_repo(test_repo_dir, init_empty_dir=True):
            raise Exception('run inside ".test_repo directory: git init --bare')
        test_no_git_path = os.path.join(test_dir, '.test_no_git')
        print('test not git path:', test_no_git_path)
        os.makedirs(test_no_git_path, exist_ok=True)
        source_test_index_html_path = os.path.join(test_dir, 'test_index.html')
        target_test_index_html_path = os.path.join(test_no_git_path, 'index.html')
        if not os.path.exists(target_test_index_html_path):
            shutil.copyfile(source_test_index_html_path, target_test_index_html_path)        
        test_site_path = os.path.join(test_dir, '.test_site')
        print('test deploy site path:', test_site_path)
        os.makedirs(test_site_path, exist_ok=True)
        target_test_index_html_path = os.path.join(test_site_path, 'index.html')
        if not os.path.exists(target_test_index_html_path):
            shutil.copyfile(source_test_index_html_path, target_test_index_html_path)
        temp_file_path = os.path.join(test_site_path, 'temp.txt')
        print('temp file path:', temp_file_path)
        with open(temp_file_path, 'w') as file:
            file.write(str(datetime.now()))
        if not is_git_repo(test_site_path, init=True, init_branch='master'):
            raise Exception('run inside ".test_site" directory: git init')
        test_wrong_branch_path = os.path.join(test_dir, '.test_wrong_branch')
        print('test wrong branch path:', test_wrong_branch_path)
        os.makedirs(test_wrong_branch_path, exist_ok=True)
        target_test_index_html_path = os.path.join(test_wrong_branch_path, 'index.html')
        if not os.path.exists(target_test_index_html_path):
            shutil.copyfile(source_test_index_html_path, target_test_index_html_path)
        if not is_git_repo(test_wrong_branch_path, init=True, init_branch='wrong'):
            raise Exception('run inside ".test_wrong_branch" directory: git init')

    def test_config(self):
        self.assertIn('deploy', self.config)
        config_deploy = self.config['deploy']
        self.assertIn('remote', config_deploy)
        deploy_remote = config_deploy['remote']
        self.assertEqual('test', deploy_remote['name'])
        self.assertEqual('.test_repo', deploy_remote['url'])
        self.assertEqual('master', config_deploy['branch'])

    def test_deploy_test_no_git(self):
        try:
            # Change to the specified directory temporarily
            original_cwd = os.getcwd()
            os.chdir(self.test_dir)
            self.assertFalse(git_deploy('.test_no_git', config_path=self.test_config_path))
        finally:
            # Change back to the original working directory
            os.chdir(original_cwd)

    def test_deploy_test_wrong_branch(self):
        try:
            # Change to the specified directory temporarily
            original_cwd = os.getcwd()
            os.chdir(self.test_dir)
            self.assertFalse(git_deploy('.test_wrong_branch', config_path=self.test_config_path))
        finally:
            # Change back to the original working directory
            os.chdir(original_cwd)

    def test_deploy_test_site(self):
        try:
            # Change to the specified directory temporarily
            original_cwd = os.getcwd()
            os.chdir(self.test_dir)
            self.assertTrue(git_deploy('.test_site', config_path=self.test_config_path))
        finally:
            # Change back to the original working directory
            os.chdir(original_cwd)

if __name__ == '__main__':
    unittest.main()