#
# RNAspace: non-coding RNA annotation platform
# Copyright (C) 2009  CNRS, INRA, INRIA, Univ. Paris-Sud 11
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from distutils.core import setup
import glob
import shutil
import os

def main():

    setup(name='rnaspace',
          version='1.0',
          description="""
          A collaborative platform for non-protein-coding RNA annotation""",
          long_description="""
          The platform allows running in an integrated environment a variety
          of ncRNA gene finders, to explore results with dedicated tools for
          comparison, visualization and edition of putative ncRNAs and to
          export them in various formats (FASTA, GFF, RNAML).
          
          See http://rnaspace.org to have an idea of an open web site 
          without user authentification.

          ``rnaspace`` requires ``CherryPy`` and ``Cheetah``.
          """,
          author="see the AUTHORS joined file",
          author_email="contact@rnaspace.org",
          url="http://rnaspace.org",
          download_url="http://sourceforge.net/projects/rnaspace/",
          keywords=["non-protein-coding RNA", "ncRNA", "annotation"],
          requires=[
              "CherryPy (>= 3.1.2)",
              "Cheetah (>= 2.0.1)",
           ],
          packages=[
            'rnaspace', 
            'rnaspace.dao', 
            'rnaspace.core',  
            'rnaspace.core.conversion', 
            'rnaspace.core.exploration',
            'rnaspace.core.prediction', 
            'rnaspace.core.prediction.wrappers', 
            'rnaspace.core.trace',
            'rnaspace.ui',
            'rnaspace.ui.controller',
            'rnaspace.ui.controller.explore', 
            'rnaspace.ui.controller.manage',
            'rnaspace.ui.controller.predict',
            'rnaspace.ui.model', 
            'rnaspace.ui.model.explore', 
            'rnaspace.ui.model.manage',
            'rnaspace.ui.model.predict',
            'rnaspace.ui.view', 
            'rnaspace.ui.view.explore', 
            'rnaspace.ui.view.manage',
            'rnaspace.ui.view.predict',
            'rnaspace.ui.utils',
            ],
          package_data={'rnaspace.ui.view': ['*.tmpl'],
                        'rnaspace.ui.view.explore': ['*.tmpl'], 
                        'rnaspace.ui.view.manage': ['*.tmpl'],
                        'rnaspace.ui.view.predict': ['*.tmpl'],
                        'rnaspace.ui': ['ressource/js/*.js',
                                        'ressource/applet/*.jar',
                                        'ressource/css/*.css',
                                        'ressource/img/*.jpg',
                                        'ressource/img/*.gif',
                                        'ressource/img/*.ico',
                                        'ressource/img/*.png',
                                        'ressource/img/css_img/*.png',
                                        'ressource/img/css_img/*.gif',
                                        'ressource/img/css_img/forms/*.png',
                                        'ressource/img/icon/*',
                                        'ressource/sample/*'
                                        ],
                        'rnaspace': ['cfg/*.cfg', 'cfg/predictors/*.conf',
                                     'docs/*.odt', 'docs/*.py'],
                        },
          scripts=['rnaspace_on_web'],
          platforms='Unix',
          license='GNU General Public License (GPL)',
          classifiers=[
            'Programming Language :: Python',
            'Operating System :: Unix',
            'Environment :: Web Environment',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Topic :: Scientific/Engineering :: Bio-Informatics'
            ]
          )

if __name__ == '__main__':
    dirname = os.path.abspath(os.path.dirname(__file__))
    docs = os.path.join(dirname, 'docs')
    conf = os.path.join(dirname, 'cfg')
    rnaspace_docs = os.path.join(dirname, 'rnaspace', 'docs')
    rnaspace_conf = os.path.join(dirname, 'rnaspace', 'cfg')

    # copy docs and cfgs into rnaspace dir.
    # allow us to install this directory in dist-package/rnaspace/
    shutil.copytree(docs, rnaspace_docs)
    shutil.copytree(conf, rnaspace_conf)
    main()
    shutil.rmtree(rnaspace_docs)
    shutil.rmtree(rnaspace_conf)
    
