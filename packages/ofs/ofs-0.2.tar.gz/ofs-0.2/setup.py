from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

try:
    fo = open('README.rst')
    long_description = fo.read()
except:
    long_description="""OFS - provides plugin-orientated low-level blobstore. """,
finally:
    fo.close()

setup(
    name="ofs",
    version="0.2",
    description="OFS - provides plugin-orientated low-level blobstore.",
    long_description=long_description,
    author="Ben O'Steen, Friedrich Lindenberg, Rufus Pollock",
    author_email="bosteen@gmail.com",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    url="http://bitbucket.org/okfn/ofs",
    packages=find_packages(),
    test_suite = "test.test.TestPairtreeOFS",
    install_Requires = ["argparse"],
    entry_points="""
    [ofs.backend]
    pairtree = ofs.local.pairtreestore:PTOFS
    mdpairtree= ofs.local.metadatastore:MDOFS
    s3 = ofs.remote.botostore:S3OFS
    google = ofs.remote.botostore:GSOFS
    archive.org = ofs.remote.botostore:ArchiveOrgOFS
    reststore = ofs.remote.reststore:RESTOFS

    [console_scripts]
    ofs_upload = ofs.command:ofs
    """
    )

