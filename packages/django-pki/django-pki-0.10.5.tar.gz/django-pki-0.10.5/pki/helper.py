import os
import tempfile
import string
import random
import zipfile
import logging

from django.utils.safestring import mark_safe

from pki.settings import PKI_DIR, MEDIA_URL
import pki.models

logger = logging.getLogger("pki")

def files_for_object(obj):
    """Return files associated to object.
    
    Return dict containing all files associated to object. Dict contains
    chain, crl, pem, csr, der, pkcs12 and key
    """
    
    if isinstance( obj, pki.models.CertificateAuthority):
        chain   = c_name = obj.name
        ca_dir  = os.path.join(PKI_DIR, obj.name)
        key_loc = os.path.join(ca_dir, 'private')
    elif isinstance( obj, pki.models.Certificate):
        chain   = obj.parent.name
        c_name  = obj.name
        ca_dir  = os.path.join(PKI_DIR, obj.parent.name)
        key_loc = os.path.join(ca_dir, 'certs')
    else:
        raise Exception( "Given object type is unknown!" )
    
    files = { 'chain' : { 'path': os.path.join(ca_dir, '%s-chain.cert.pem' % chain),
                          'name': '%s-chain.cert.pem' % chain,
                        },
              'crl'   : { 'path': os.path.join(ca_dir, 'crl', '%s.crl.pem' % c_name),
                          'name': '%s.crl.pem' % c_name,
                        },
              'pem'   : { 'path': os.path.join(ca_dir, 'certs', '%s.cert.pem' % c_name),
                          'name': '%s.cert.pem' % c_name,
                        },
              'csr'   : { 'path': os.path.join(ca_dir, 'certs', '%s.csr.pem' % c_name),
                          'name': '%s.csr.pem' % c_name,
                        },
              'der'   : { 'path': os.path.join(ca_dir, 'certs', '%s.cert.der' % c_name),
                          'name': '%s.cert.der' % c_name,
                        },
              'pkcs12': { 'path': os.path.join(ca_dir, 'certs', '%s.cert.p12' % c_name),
                          'name': '%s.cert.p12' % c_name,
                        },
              'key'   : { 'path': os.path.join(ca_dir, key_loc, '%s.key.pem' % c_name),
                          'name': '%s.key.pem' % c_name,
                        },
            }
    
    return files

def subject_for_object(obj):
    """Return a subject string.
    
    A OpenSSL compatible subject string is returned.
    """
    
    subj = '/CN=%s/C=%s/ST=%s/localityName=%s/O=%s' % ( obj.common_name,
                                                        obj.country,
                                                        obj.state,
                                                        obj.locality,
                                                        obj.organization,
                                                      )
    
    if obj.OU:
        subj += '/organizationalUnitName=%s' % obj.OU
    
    if obj.email:
        subj += '/emailAddress=%s' % obj.email
    
    return subj

def chain_recursion(r_id, store, id_dict):
    """Helper function for recusion"""
    
    i = pki.models.CertificateAuthority.objects.get(pk=r_id)
    
    div_content = build_delete_item(i)
    store.append( mark_safe('Certificate Authority: <a href="../../%d/">%s</a> <img src="%spki/img/plus.png" class="switch" /><div class="details">%s</div>' % (i.pk, i.name, MEDIA_URL, div_content)) )
    
    id_dict['ca'].append(i.pk)
    
    ## Search for child certificates
    child_certs = pki.models.Certificate.objects.filter(parent=r_id)
    if child_certs:
        helper = []
        for cert in child_certs:
            div_content = build_delete_item(cert)
            helper.append( mark_safe('Certificate: <a href="../../../certificate/%d/">%s</a> <img src="%spki/img/plus.png" class="switch" /><div class="details">%s</div>' % (cert.pk, cert.name, MEDIA_URL, div_content)) )
            id_dict['cert'].append(cert.pk)
        store.append(helper)
    
    ## Search for related CA's
    child_cas = pki.models.CertificateAuthority.objects.filter(parent=r_id)
    if child_cas:
        helper = []
        for ca in child_cas:
            chain_recursion(ca.pk, helper, id_dict)
        store.append(helper)

def build_delete_item(obj):
    """Build div tag for delete details"""
    
    parent = 'None'
    if obj.parent is not None:
        parent = obj.parent.name
    
    return "<ul><li>Serial: %s</li><li>Subject: %s</li><li>Parent: %s</li><li>Description: %s</li><li>Created: %s</li><li>Expiry date: %s</li></ul>" % ( obj.serial, subject_for_object(obj), parent, obj.description, obj.created, obj.expiry_date)

def generate_temp_file():
    """Generate a filename in the systems temp directory"""
    
    f = os.path.join(tempfile.gettempdir(), "".join(random.sample(string.letters+string.digits, 25)))
    
    if os.path.exists(f):
        raise Exception( "The generated temp file %s already exists!" % f )
    
    return f

def build_zip_for_object(obj, request):
    """Build zip with filed ob object.
    
    request is required to check permissions. Zip file path is returned.
    """
    
    try:
        ## Create the ZIP archive
        base_folder = 'PKI_DATA_%s' % obj.name
        files       = files_for_object(obj)
        zip_f       = generate_temp_file()
        
        c_zip = zipfile.ZipFile(zip_f, 'w')
        
        ## Private key is only included if user has permission
        if not request.user.has_perm('pki.can_download_%s' % type):
            logger.error( "Permission denied: Private key is excluded" )
        else:
            logger.debug( "Access granted. User is allowed to download private key" )
            c_zip.write( files['key']['path'], files['key']['name'] )
        
        c_zip.write( files['pem']['path'], files['pem']['name'] )
        c_zip.write( files['chain']['path'], files['chain']['name'])
        
        try:
            if obj.pkcs12_encoded:
                c_zip.write( files['pkcs12']['path'], files['pkcs12']['name'] )
        except AttributeError:
            pass
        
        if obj.der_encoded:
            c_zip.write( files['der']['path'], files['der']['name'] )
        
        c_zip.close()
    except Exception, e:
        logger.error( "Exception during zip file creation: %s" % e )
        raise Exception( e )
    
    return zip_f

