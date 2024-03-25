FROM ghcr.io/void-linux/void-musl:d1ee412

RUN xbps-install -Suy \
	make \
	gcc \
	shadow \
	python3 \
	python3-async-timeout \
	python3-GitPython \
	python3-colorama \
	python3-dateutil \
	python3-pytz \
	python3-grpcio \
	python3-google-api-core \
	python3-google-api-python-client \
	python3-google-auth \
	python3-google-auth-oauthlib \
	python3-Pillow \
	python3-pynacl \
	python3-requests \
	python3-six \
	python3-virtualenv \
	python3-youtube-dl

# Can't do non-rootless user because we can't mount the various config files as
# a non-root user. If we ignore the write operations then this would work just
# fine
# RUN useradd --create-home --shell /bin/sh app
# USER app

WORKDIR /app

RUN virtualenv --system-site-packages venv
ADD requirements.txt requirements.txt
RUN venv/bin/pip install -r requirements.txt

COPY main.py bot.py palette.png ./
COPY utils ./utils
RUN cd utils && make
COPY bc_funcs ./bc_funcs
COPY cogs ./cogs

CMD [ "venv/bin/python3", "./main.py" ]
