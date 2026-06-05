"""Locale helpers for ServerCommander MCP tool metadata."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any

DEFAULT_LOCALE = "en"
SUPPORTED_LOCALES = ("en", "de", "es", "zh", "ja", "ru")

ALIASES = {
    "en-us": "en",
    "en-gb": "en",
    "de-de": "de",
    "de-at": "de",
    "de-ch": "de",
    "es-es": "es",
    "es-mx": "es",
    "zh-cn": "zh",
    "zh-hans": "zh",
    "ja-jp": "ja",
    "ru-ru": "ru",
    "ru-by": "ru",
    "zh-sg": "zh",
    "zh-hk": "zh",
    "zh-tw": "zh",
    "es-419": "es",
    "es-ar": "es",
    "es-cl": "es",
    "es-co": "es",
}

DEFAULT_SCHEMA_DESCRIPTIONS: dict[str, str] = {
    "body": "Email body text.",
    "dry_run": "Build the plan without executing deployment.",
    "endpoints": "HTTP endpoint URLs to check.",
    "folder": "Mail folder name.",
    "format": "Log format hint.",
    "limit": "Maximum number of results.",
    "local_path": "Local source path.",
    "log_path": "Local access-log file path.",
    "log_text": "Inline access-log text.",
    "message_id": "Message identifier.",
    "profile": "Deployment profile name.",
    "query": "Search query.",
    "remote_path": "Remote target path.",
    "subject": "Email subject.",
    "timeout": "Request timeout in seconds.",
    "to": "Email recipient.",
    "top_paths": "Number of top paths to include.",
}

SCHEMA_TRANSLATIONS: dict[str, dict[str, str]] = {
    "de": {
        "body": "Textkörper der E-Mail.",
        "dry_run": "Plan erstellen, ohne das Deployment auszuführen.",
        "endpoints": "Zu prüfende HTTP-Endpunkt-URLs.",
        "folder": "Name des Mail-Ordners.",
        "format": "Hinweis auf das Logformat.",
        "limit": "Maximale Anzahl von Ergebnissen.",
        "local_path": "Lokaler Quellpfad.",
        "log_path": "Lokaler Pfad zur Access-Log-Datei.",
        "log_text": "Access-Log-Text direkt als Eingabe.",
        "message_id": "Nachrichtenkennung.",
        "profile": "Name des Deployment-Profils.",
        "query": "Suchanfrage.",
        "remote_path": "Entfernter Zielpfad.",
        "subject": "E-Mail-Betreff.",
        "timeout": "Request-Timeout in Sekunden.",
        "to": "E-Mail-Empfänger.",
        "top_paths": "Anzahl der wichtigsten Pfade.",
    },
    "es": {
        "body": "Texto del cuerpo del correo.",
        "dry_run": "Crear el plan sin ejecutar el despliegue.",
        "endpoints": "URLs de endpoints HTTP a comprobar.",
        "folder": "Nombre de la carpeta de correo.",
        "format": "Pista sobre el formato del log.",
        "limit": "Número máximo de resultados.",
        "local_path": "Ruta local de origen.",
        "log_path": "Ruta local del archivo de access log.",
        "log_text": "Texto de access log en línea.",
        "message_id": "Identificador del mensaje.",
        "profile": "Nombre del perfil de despliegue.",
        "query": "Consulta de búsqueda.",
        "remote_path": "Ruta remota de destino.",
        "subject": "Asunto del correo.",
        "timeout": "Timeout de la petición en segundos.",
        "to": "Destinatario del correo.",
        "top_paths": "Cantidad de rutas principales a incluir.",
    },
    "zh": {
        "body": "邮件正文。",
        "dry_run": "只生成计划，不执行部署。",
        "endpoints": "要检查的 HTTP 端点 URL。",
        "folder": "邮件文件夹名称。",
        "format": "日志格式提示。",
        "limit": "最大结果数量。",
        "local_path": "本地源路径。",
        "log_path": "本地访问日志文件路径。",
        "log_text": "内联访问日志文本。",
        "message_id": "消息标识符。",
        "profile": "部署配置名称。",
        "query": "搜索查询。",
        "remote_path": "远程目标路径。",
        "subject": "邮件主题。",
        "timeout": "请求超时时间（秒）。",
        "to": "邮件收件人。",
        "top_paths": "要包含的热门路径数量。",
    },
    "ja": {
        "body": "メール本文。",
        "dry_run": "デプロイを実行せずに計画を作成します。",
        "endpoints": "確認する HTTP エンドポイント URL。",
        "folder": "メールフォルダ名。",
        "format": "ログ形式のヒント。",
        "limit": "結果の最大数。",
        "local_path": "ローカルのソースパス。",
        "log_path": "ローカルのアクセスログファイルパス。",
        "log_text": "インラインのアクセスログテキスト。",
        "message_id": "メッセージ識別子。",
        "profile": "デプロイプロファイル名。",
        "query": "検索クエリ。",
        "remote_path": "リモートの宛先パス。",
        "subject": "メール件名。",
        "timeout": "リクエストタイムアウト（秒）。",
        "to": "メール受信者。",
        "top_paths": "含める上位パスの数。",
    },
    "ru": {
        "body": "Текст письма.",
        "dry_run": "Создать план без выполнения деплоя.",
        "endpoints": "URL HTTP endpoints для проверки.",
        "folder": "Название почтовой папки.",
        "format": "Подсказка формата лога.",
        "limit": "Максимальное количество результатов.",
        "local_path": "Локальный исходный путь.",
        "log_path": "Локальный путь к access-log файлу.",
        "log_text": "Текст access-log напрямую.",
        "message_id": "Идентификатор сообщения.",
        "profile": "Название профиля деплоя.",
        "query": "Поисковый запрос.",
        "remote_path": "Удаленный целевой путь.",
        "subject": "Тема письма.",
        "timeout": "Таймаут запроса в секундах.",
        "to": "Получатель письма.",
        "top_paths": "Количество популярных путей.",
    },
}

TRANSLATIONS: dict[str, dict[str, str]] = {
    "de": {
        "tool.sc_deploy": "Erstellt einen sicheren Deployment-Plan. Alpha: Ausführung nur als Dry-run.",
        "tool.sc_deploy_status": "Zeigt konfigurierte Deployment-Profile und Alpha-History-Status.",
        "tool.sc_mail_list": "Alpha-Mail-Status für das Auflisten eines IMAP-Ordners.",
        "tool.sc_mail_read": "Alpha-Mail-Status für das Lesen einer Nachricht.",
        "tool.sc_mail_send": "Alpha-Mail-Status für das Senden einer E-Mail; sendet noch nicht.",
        "tool.sc_mail_search": "Alpha-Mail-Status für die Mail-Suche.",
        "tool.sc_logs_analyze": "Analysiert Apache-/Nginx-Access-Logs aus Text oder Datei.",
        "tool.sc_health_check": "Prüft HTTP-Endpunkte und meldet Status-Codes plus Latenz.",
        "error.unknown_tool": "Unbekanntes ServerCommander-Tool: {name}",
    },
    "es": {
        "tool.sc_deploy": "Crea un plan de despliegue seguro. Alpha: solo dry-run.",
        "tool.sc_deploy_status": "Muestra perfiles de despliegue y estado de historial alpha.",
        "tool.sc_mail_list": "Estado alpha para listar una carpeta IMAP.",
        "tool.sc_mail_read": "Estado alpha para leer un mensaje.",
        "tool.sc_mail_send": "Estado alpha para enviar correo; aún no envía.",
        "tool.sc_mail_search": "Estado alpha para buscar correo.",
        "tool.sc_logs_analyze": "Analiza logs de acceso Apache/Nginx desde texto o archivo.",
        "tool.sc_health_check": "Comprueba endpoints HTTP y devuelve código de estado y latencia.",
        "error.unknown_tool": "Herramienta ServerCommander desconocida: {name}",
    },
    "zh": {
        "tool.sc_deploy": "创建安全部署计划。Alpha 版仅支持 dry-run。",
        "tool.sc_deploy_status": "显示部署配置和 Alpha 历史状态。",
        "tool.sc_mail_list": "用于列出 IMAP 文件夹的 Alpha 邮件状态。",
        "tool.sc_mail_read": "用于读取邮件的 Alpha 状态。",
        "tool.sc_mail_send": "用于发送邮件的 Alpha 状态；当前不会真正发送。",
        "tool.sc_mail_search": "用于搜索邮件的 Alpha 状态。",
        "tool.sc_logs_analyze": "从文本或文件分析 Apache/Nginx 访问日志。",
        "tool.sc_health_check": "检查 HTTP 端点并返回状态码和延迟。",
        "error.unknown_tool": "未知 ServerCommander 工具：{name}",
    },
    "ja": {
        "tool.sc_deploy": "安全なデプロイ計画を作成します。Alpha では dry-run のみです。",
        "tool.sc_deploy_status": "設定済みデプロイプロファイルと Alpha 履歴状態を表示します。",
        "tool.sc_mail_list": "IMAP フォルダ一覧用の Alpha メール状態を返します。",
        "tool.sc_mail_read": "メッセージ読み取り用の Alpha メール状態を返します。",
        "tool.sc_mail_send": "メール送信用の Alpha 状態を返します。まだ送信しません。",
        "tool.sc_mail_search": "メール検索用の Alpha 状態を返します。",
        "tool.sc_logs_analyze": "テキストまたはファイルから Apache/Nginx アクセスログを分析します。",
        "tool.sc_health_check": "HTTP エンドポイントを確認し、ステータスコードとレイテンシを返します。",
        "error.unknown_tool": "不明な ServerCommander ツール: {name}",
    },
    "ru": {
        "tool.sc_deploy": "Создает безопасный план деплоя. Alpha: только dry-run.",
        "tool.sc_deploy_status": "Показывает профили деплоя и alpha-статус истории.",
        "tool.sc_mail_list": "Alpha-статус для просмотра папки IMAP.",
        "tool.sc_mail_read": "Alpha-статус для чтения сообщения.",
        "tool.sc_mail_send": "Alpha-статус отправки почты; пока не отправляет.",
        "tool.sc_mail_search": "Alpha-статус поиска почты.",
        "tool.sc_logs_analyze": "Анализирует access-логи Apache/Nginx из текста или файла.",
        "tool.sc_health_check": "Проверяет HTTP endpoints и возвращает коды статуса и задержку.",
        "error.unknown_tool": "Неизвестный инструмент ServerCommander: {name}",
    },
}


def normalize_locale(locale: str | None) -> str:
    if not locale:
        return DEFAULT_LOCALE
    normalized = locale.strip().lower().replace("_", "-")
    normalized = ALIASES.get(normalized, normalized.split("-", 1)[0])
    if normalized in SUPPORTED_LOCALES:
        return normalized
    return DEFAULT_LOCALE


@dataclass(frozen=True)
class I18n:
    locale: str = DEFAULT_LOCALE

    def __post_init__(self) -> None:
        object.__setattr__(self, "locale", normalize_locale(self.locale))

    def t(self, key: str, default: str | None = None) -> str:
        if self.locale == DEFAULT_LOCALE:
            return default or key
        return TRANSLATIONS.get(self.locale, {}).get(key) or default or key

    def localize_schema(self, schema: dict[str, Any]) -> dict[str, Any]:
        """Return a copy of a JSON schema with localized property descriptions."""
        localized = deepcopy(schema)
        properties = localized.get("properties")
        if isinstance(properties, dict):
            for name, property_schema in properties.items():
                if not isinstance(property_schema, dict):
                    continue
                description = self._schema_description(name, property_schema.get("description"))
                if description:
                    property_schema["description"] = description
        return localized

    def _schema_description(self, name: str, default: str | None = None) -> str | None:
        fallback = default or DEFAULT_SCHEMA_DESCRIPTIONS.get(name)
        if self.locale == DEFAULT_LOCALE:
            return fallback
        return SCHEMA_TRANSLATIONS.get(self.locale, {}).get(name) or fallback
