FROM continuumio/anaconda3:2022.10

WORKDIR /pkl/projects/rec_sys/user_based/book_rec_sys/

COPY . .

RUN pip install -r requirements.txt

CMD python app.py
