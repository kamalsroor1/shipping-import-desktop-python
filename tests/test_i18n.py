"""
Unit Tests for Internationalization Engine (i18n)
Tests language switching between Pure Arabic (ar) and Pure English (en).
"""

from src.utils.i18n import i18n


def test_i18n_arabic_translations():
    i18n.set_language("ar")
    assert i18n.current_lang == "ar"
    assert i18n.t("app_name") == "نظام إدارة الاستيراد"
    assert i18n.t("btn_refresh_data") == "🔄 تحديث البيانات"


def test_i18n_english_translations():
    i18n.set_language("en")
    assert i18n.current_lang == "en"
    assert i18n.t("app_name") == "Import Management System"
    assert i18n.t("btn_refresh_data") == "🔄 Refresh Data"
    # Revert to Arabic default
    i18n.set_language("ar")
