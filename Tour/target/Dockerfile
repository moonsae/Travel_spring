FROM tomcat:9.0-jdk11-openjdk-slim

ENV PROFILE="dev"

# WAR 파일을 Tomcat의 웹 애플리케이션 디렉터리로 복사하고 이름을 'tour.war'로 변경
COPY tour-1.0.0-BUILD-SNAPSHOT.war /usr/local/tomcat/webapps/tour.war

# Tomcat 서버 실행
CMD ["catalina.sh", "run"]
