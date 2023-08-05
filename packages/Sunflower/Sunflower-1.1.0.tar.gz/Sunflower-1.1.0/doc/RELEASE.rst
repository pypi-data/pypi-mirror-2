======================
 Release instructions
======================
::

  SETUP_VERSION=$(python setup.py --version)

  svn update
  svn commit -m "preparing for release ${SETUP_VERSION}"
  python setup.py release

  easy_install dist/Sunflower-${SETUP_VERSION}.tar.gz

  # test here

  pushd dist
  tar zxvf Sunflower-${SETUP_VERSION}.tar.gz # for "release source"
  popd

  pushd doc
  make latex && make -C _build/latex all-pdf && evince _build/latex/*.pdf
  popd

  REPOS_ROOT=$(svn info . | fgrep "Repository Root: " | cut -d " " -f 3)
  svn cp -m "release ${SETUP_VERSION}" \
      . ${REPOS_ROOT}/tags/release-${SETUP_VERSION}
  command emacs setup.py NEWS.rst # increase version number
  svn commit -m "incrementing version"

  scp dist/Sunflower-1.0.1.tar.gz doc/_build/latex/Sunflower.pdf \
      waterlily:~/public_html/software/sunflower
  rsync -r doc/_build/html/ waterlily:~/public_html/software/sunflower/doc
