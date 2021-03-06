#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)
import boto3, re
from time import gmtime, strftime

def detect_text(image='control.png', bucket='aiimageseducate', statement=''):
    rw_log = open("rejected_words", "a")

    client = boto3.client(
        'rekognition',
        # Hard coded strings as credentials, not recommended.
        aws_access_key_id="",
        aws_secret_access_key="",
        aws_session_token=""
        )
    try:
        response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':image}})
    except:
        print(f"error! image {image} or bucket {bucket} not found, check it!")    
        return f"error! image {image} or bucket {bucket} not found, check it!", 0                
    textDetections=response['TextDetections']

    words = 0
    average_confidence = 0
    statement_detected = ''
    original_statement = ''

    rw_log.write(f"file: {image}\n---------------\n")
    for text in textDetections:
        if  (text['Type'] == "WORD"):
             continue
        Detected_text = text['DetectedText'].lower().strip()
        Detected_text = re.sub('\W+','', Detected_text )
        
        if (text['Confidence']>97 or Detected_text in statement):
            statement_detected += f"{Detected_text} "
            original_statement += f"{text['DetectedText']} "
            average_confidence += text['Confidence']
            words +=1
        else:
            rw_log.write(f"word: {Detected_text}, confidence: {text['Confidence']} \n")

    rw_log.write(f"-------------------------------------------------\n")
    rw_log.close()
    average_confidence = round(average_confidence/words) if words != 0 else 0
    statement_detected = ''.join(statement_detected.lower()[:-1].split(' '))
    statement_detected = statement_detected if statement_detected != '' else 'null'
    return statement_detected, average_confidence, original_statement

def main():

    time_test = strftime("%d/%b/%Y %H:%M:%S", gmtime())
    rw_log = open("rejected_words", "w") # create logs rejected words
    rw_log.write(f"time log: {time_test} \n")
    rw_log.close()
    logs = open("Logs", "w")
    logs.write(f"time log: {time_test} \n")

    statement_detected, average_confidence, original_statement = detect_text()
    logs.write(f"control statement: {original_statement}\n\t|average_confidence: {average_confidence}% \n")

    logs.write(f"---------------------------------------------------------------------------------------------------------------------\n")
    images = ['test.png', 'test2.jpg', 'test3.jpg', 'test4.jpg', 'test5.jpg', 'test6.jpg', 'test7.jpg', 'test8.png', 'test9.jpg', 'test10.jpg', 'test11.jpg', 'test12.jpg', 'test13.jpg', 'test14.png', 'test15.png']
    # images = ['test9.jpg']
    for image in images:
        logs.write(f"Test image: {image}:\n")

        statement_detected2, average_confidence2, original_statement2 = detect_text(image=image, statement=statement_detected)

        logs.write(f"\t|Test statement: {original_statement2}\n\t\t|average_confidence: {average_confidence2}% \n")
        print(f"Texto de imagen de prueba {'SI' if statement_detected2 in statement_detected else 'NO'} está completamente presente en el texto de imagen de control.")
        logs.write(f"\t|found text: {statement_detected2 in statement_detected}.\n")
        logs.write(f"---------------------------------------------------------------------------------------------------------------------\n")

    logs.close()

if __name__ == "__main__":
    main()