FROM python:3.13

RUN pip install \
		isort \
		mypy \
		ruff

WORKDIR /home/user/src/

COPY requirements.txt /home/user/src/

RUN pip install -r requirements.txt

COPY . /home/user/src/

# Set the default command to bash.
CMD ["bash"]
