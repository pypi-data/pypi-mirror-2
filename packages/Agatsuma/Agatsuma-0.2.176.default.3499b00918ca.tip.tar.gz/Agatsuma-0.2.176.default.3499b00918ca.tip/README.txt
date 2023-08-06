Minimal installation script:
============================

    #!/bin/sh

    export ENVNAME=venv

    if [ -d $ENVNAME ]; then
        rm -rf ./$ENVNAME
    fi

    virtualenv $ENVNAME

    pip install -E $ENVNAME pyyaml

    export AGATSUMA_CONF="--without-sqla --without-memcache --without-mongo --without-tornado --without-pylons"
    pip install -E $ENVNAME --log=log.txt --upgrade agatsuma
