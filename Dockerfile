ARG BASE=centos:7.6.1810

FROM $BASE as common
RUN yum install -y httpd


FROM common as build

# httpd-devel and gcc are to support building mod_wsgi from source.
RUN yum install -y httpd-devel gcc

# miniconda
RUN curl --silent --location -o /miniconda-installer.sh \
    https://repo.anaconda.com/miniconda/Miniconda3-py310_22.11.1-1-Linux-x86_64.sh
RUN bash /miniconda-installer.sh -b -p /conda
RUN eval "$('/conda/bin/conda' 'shell.bash' 'hook' 2> /dev/null)" && \
    conda config --set auto_update_conda False && \
    conda install -c conda-forge conda==23.1.0 conda-lock==1.4.0

# build conda environment
COPY conda-lock.yml /build/conda-lock.yml
RUN eval "$('/conda/bin/conda' 'shell.bash' 'hook' 2> /dev/null)" && \
    conda-lock install --no-dev -n app /build/conda-lock.yml && \
    conda clean -afy

# mod_wsgi: use pip to compile mod_wsgi from source for the particular versions
# of apache and python that we're using.
RUN eval "$('/conda/bin/conda' 'shell.bash' 'hook' 2> /dev/null)" && \
    conda activate app && \
    pip install mod_wsgi==4.9.4



FROM common

COPY --from=build /conda /conda

# httpd config
COPY docker/httpd.conf /etc/httpd/conf/httpd.conf

# The following is bad security practice if running httpd as
# root, but we will run it as apache.
RUN chmod g+rwx /run/httpd

# install application
COPY miniauth.py docker/app.wsgi docker/entrypoint docker/service /app/

USER apache:apache
WORKDIR /app
ENTRYPOINT ["/app/entrypoint"]
CMD ["/app/service"]
