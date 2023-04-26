FROM fastai/fastai
RUN python3 -m pip install flask gunicorn
WORKDIR /models
ENTRYPOINT ["gunicorn", "app:app", "-w", "1", "--threads", "1", "-b", "0.0.0.0:5000"]


#gunicorn app:app -w 1 --threads 1 -b 0.0.0.0:5000

#docker build -t flaskai:0.01 .