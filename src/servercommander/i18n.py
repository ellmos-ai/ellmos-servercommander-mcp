"""Locale helpers for ServerCommander MCP tool metadata."""

from __future__ import annotations

from dataclasses import dataclass

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
