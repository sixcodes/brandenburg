FROM python:3.7.8-slim

COPY . /opt/app
WORKDIR /opt/app

RUN set -ex \
	&& buildDeps="build-essential" \
	&& apt-get update \
    && apt-get install -y $buildDeps --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && pip install -U pip==18.1 pipenv==2018.10.13 \
    && pipenv install --system --deploy --ignore-pipfile \
    && apt-get purge -y --auto-remove $buildDeps \
    && find /usr/local -depth \
		\( \
			\( -type d -a \( -name test -o -name tests \) \) \
			-o \
			\( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
            \) -exec rm -rf '{}' +
EXPOSE 8000

CMD ["uvicorn", "brandenburg.main:app"]
