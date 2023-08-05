from __future__ import absolute_import

import os
import mock
import httplib2
from nose.tools import assert_raises
from cloudservers.shell import CloudserversShell, CommandError
from .fakeserver import FakeServer

# Patch os.environ to avoid required auth info.
def setup():
    global _old_env
    fake_env = {
        'CLOUD_SERVERS_USERNAME': 'username',
        'CLOUD_SERVERS_API_KEY': 'password'
    }
    _old_env, os.environ = os.environ, fake_env.copy()

    # Make a fake shell object, a helping wrapper to call it, and a quick way
    # of asserting that certain API calls were made.
    global shell, _shell, assert_called
    _shell = CloudserversShell()
    _shell._api_class = FakeServer
    assert_called = lambda m, u, b=None: _shell.cs.assert_called(m, u, b)
    shell = lambda cmd: _shell.main(cmd.split())

def teardown():
    global _old_env
    os.environ = _old_env

def test_backup_schedule():
    shell('backup-schedule 1234')
    assert_called('GET', '/servers/1234/backup_schedule')  
      
    shell('backup-schedule sample-server --weekly monday')
    assert_called(
        'POST', '/servers/1234/backup_schedule',
        {'backupSchedule': {'enabled': True, 'daily': 'DISABLED', 
                            'weekly': 'MONDAY'}}
    )
    
    shell('backup-schedule sample-server --weekly disabled --daily h_0000_0200')
    assert_called(
        'POST', '/servers/1234/backup_schedule',
        {'backupSchedule': {'enabled': True, 'daily': 'H_0000_0200', 
                            'weekly': 'DISABLED'}}
    )
    
    shell('backup-schedule sample-server --disable')
    assert_called(
        'POST', '/servers/1234/backup_schedule',
        {'backupSchedule': {'enabled': False, 'daily': 'DISABLED', 
                            'weekly': 'DISABLED'}}
    )

def test_backup_schedule_delete():
    shell('backup-schedule-delete 1234')
    assert_called('DELETE', '/servers/1234/backup_schedule')

def test_boot():
    shell('boot --image 1 some-server')
    assert_called(
        'POST', '/servers',
        {'server': {'flavorId': 1, 'name': 'some-server', 'imageId': 1}}
    )

    shell('boot --image 1 --meta foo=bar --meta spam=eggs some-server ')
    assert_called(
        'POST', '/servers',
        {'server': {'flavorId': 1, 'name': 'some-server', 'imageId': 1, 
                   'metadata': {'foo': 'bar', 'spam': 'eggs'}}}
    )

def test_flavor_list():
    shell('flavor-list')
    assert_called('GET', '/flavors/detail')
    
def test_image_list():
    shell('image-list')
    assert_called('GET', '/images/detail')

def test_image_create():
    shell('image-create sample-server new-image')
    assert_called(
        'POST', '/images',
        {'image': {'name': 'new-image', 'serverId': 1234}}
    )
    
def test_image_delete():
    shell('image-delete 1')
    assert_called('DELETE', '/images/1')

def test_ip_share():
    shell('ip-share sample-server 1 1.2.3.4')
    assert_called(
        'PUT', '/servers/1234/ips/public/1.2.3.4',
        {'shareIp': {'sharedIpGroupId': 1, 'configureServer': True}}
    )
    
def test_ip_unshare():
    shell('ip-unshare sample-server 1.2.3.4')
    assert_called('DELETE', '/servers/1234/ips/public/1.2.3.4')
    
def test_ipgroup_list():
    shell('ipgroup-list')
    assert_called('GET', '/shared_ip_groups/detail')
    
def test_ipgroup_show():
    shell('ipgroup-show 1')
    assert_called('GET', '/shared_ip_groups/1')
    shell('ipgroup-show group2')
    # does a search, not a direct GET
    assert_called('GET', '/shared_ip_groups/detail')
    
def test_ipgroup_create():
    shell('ipgroup-create a-group')
    assert_called(
        'POST', '/shared_ip_groups',
        {'sharedIpGroup': {'name': 'a-group'}}
    )
    shell('ipgroup-create a-group sample-server')
    assert_called(
        'POST', '/shared_ip_groups',
        {'sharedIpGroup': {'name': 'a-group', 'server': 1234}}
    )
    
def test_ipgroup_delete():
    shell('ipgroup-delete group1')
    assert_called('DELETE', '/shared_ip_groups/1')
    
def test_list():
    shell('list')
    assert_called('GET', '/servers/detail')

def test_reboot():
    shell('reboot sample-server')
    assert_called('POST', '/servers/1234/action', {'reboot': {'type': 'SOFT'}})
    shell('reboot sample-server --hard')
    assert_called('POST', '/servers/1234/action', {'reboot': {'type': 'HARD'}})
    
def test_rebuild():
    shell('rebuild sample-server 1')
    assert_called('POST', '/servers/1234/action', {'rebuild': {'imageId': 1}})

def test_rename():
    shell('rename sample-server newname')
    assert_called('PUT', '/servers/1234', {'server': {'name':'newname'}})

def test_resize():
    shell('resize sample-server 1')
    assert_called('POST', '/servers/1234/action', {'resize': {'flavorId': 1}})

def test_resize_confirm():
    shell('resize-confirm sample-server')
    assert_called('POST', '/servers/1234/action', {'confirmResize': None})
    
def test_resize_revert():
    shell('resize-revert sample-server')
    assert_called('POST', '/servers/1234/action', {'revertResize': None})

@mock.patch('getpass.getpass', mock.Mock(return_value='p'))
def test_root_password():
    shell('root-password sample-server')
    assert_called('PUT', '/servers/1234', {'server': {'adminPass':'p'}})
    
def test_show():
    shell('show 1234')
    # XXX need a way to test multiple calls
    # assert_called('GET', '/servers/1234')
    assert_called('GET', '/images/2')
    
def test_delete():
    shell('delete 1234')
    assert_called('DELETE', '/servers/1234')
    shell('delete sample-server')
    assert_called('DELETE', '/servers/1234')
    
def test_help():
    with mock.patch_object(_shell.parser, 'print_help') as m:
        shell('help')
        m.assert_called()
    with mock.patch_object(_shell.subcommands['delete'], 'print_help') as m:
        shell('help delete')
        m.assert_called()
    assert_raises(CommandError, shell, 'help foofoo')

def test_debug():
    httplib2.debuglevel = 0
    shell('--debug list')
    assert httplib2.debuglevel == 1