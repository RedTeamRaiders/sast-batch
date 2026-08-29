FROM eclipse-temurin:17-jre-jammy

RUN apt-get update && apt-get install -y --no-install-recommends curl unzip git \
    && curl -fsSL "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o /tmp/awscliv2.zip \
    && unzip -q /tmp/awscliv2.zip -d /tmp && /tmp/aws/install \
    && rm -rf /tmp/awscliv2.zip /tmp/aws \
    && VERSION=$(curl -fsSL https://dependency-check.github.io/DependencyCheck/current.txt) \
    && curl -fsSL "https://github.com/dependency-check/DependencyCheck/releases/download/v${VERSION}/dependency-check-${VERSION}-release.zip" -o /tmp/dc.zip \
    && unzip -q /tmp/dc.zip -d /opt \
    && rm /tmp/dc.zip \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/opt/dependency-check/bin:${PATH}"

COPY dependency_check_entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
