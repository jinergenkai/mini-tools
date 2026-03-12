import { useState } from "react";
import { useTranslation } from "react-i18next";
import { useTheme } from "../ThemeProvider";
import {
  Menu,
  X,
  MessageSquare,
  Globe,
  Moon,
  Sun,
  ChevronDown,
  Logo
} from "@/components/modules/icon.module";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  Button,
} from "@/components/modules/shadcn.module";

const services = [
  { name: "camera-tracking", href: "/ai-service/camera-tracking" },
  { name: "vision-asking", href: "/ai-service/vision-asking" },
  { name: "data-analytics", href: "#data-analytics" },
  { name: "voice-recognition", href: "#voice-recognition" },
  { name: "video-processing", href: "#video-processing" },
  { name: "predictive-modeling", href: "#predictive-modeling" }
];

const languages = [
  { name: "English", code: "en" },
  { name: "Tiếng Việt", code: "vi" }
];

const Header = () => {
  const { theme, setTheme } = useTheme();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { t, i18n } = useTranslation();
  const [currentLanguage, setCurrentLanguage] = useState(
    languages.find(lang => lang.code === i18n.language)?.name || "English"
  );

  const handleLanguageChange = (langName: string) => {
    const lang = languages.find(l => l.name === langName);
    if (lang) {
      void i18n.changeLanguage(lang.code);
      setCurrentLanguage(langName);
    }
  };

  const toggleTheme = () => {
    setTheme(theme === "dark" ? "light" : "dark");
  };

  return (
    <header className="fixed w-full z-50 glass-effect">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between py-4">
          {/* Logo with Home Link */}
          <a href="/" className="hover:opacity-80 transition-opacity">
            <Logo />
          </a>
          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {/* AI Services Dropdown */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="flex items-center space-x-1">
                  <span>{t('header.aiServices')}</span>
                  <ChevronDown className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-56">
                {services.map((service) => (
                  <DropdownMenuItem key={service.name} asChild>
                    <a href={service.href} className="w-full cursor-pointer">
                      {t(`header.services.${service.name}`)}
                    </a>
                  </DropdownMenuItem>
                ))}
              </DropdownMenuContent>
            </DropdownMenu>

            {/* Contact Us */}
            <Button variant="ghost" className="flex items-center space-x-2" asChild>
              <a href="/contact">
                <MessageSquare className="h-4 w-4" />
                <span>{t('header.contactUs')}</span>
              </a>
            </Button>

            {/* Language Selector */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="flex items-center space-x-2">
                  <Globe className="h-4 w-4" />
                  <span>{currentLanguage}</span>
                  <ChevronDown className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                {languages.map((language) => (
                  <DropdownMenuItem
                    key={language.code}
                    onClick={() => handleLanguageChange(language.name)}
                  >
                    {language.name}
                  </DropdownMenuItem>
                ))}
              </DropdownMenuContent>
            </DropdownMenu>

            {/* Theme Toggle */}
            <Button variant="ghost" onClick={toggleTheme} size="icon">
              {theme === "dark" ? (
                <Sun className="h-5 w-5" />
              ) : (
                <Moon className="h-5 w-5" />
              )}
            </Button>
          </nav>

          {/* Mobile Menu Button */}
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? (
              <X className="h-6 w-6" />
            ) : (
              <Menu className="h-6 w-6" />
            )}
          </Button>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="glass-effect md:hidden py-4">
          <div className="container mx-auto px-4 space-y-4">
            {/* Mobile AI Services */}
            <div className="space-y-2">
              <p className="font-medium">{t('header.aiServices')}</p>
              <div className="space-y-1 pl-4">
                {services.map((service) => (
                  <a
                    key={service.name}
                    href={service.href}
                    className="block py-1"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    {t(`header.services.${service.name}`)}
                  </a>
                ))}
              </div>
            </div>

            {/* Mobile Contact Us */}
            <Button variant="ghost" className="flex items-center space-x-2 w-full justify-start" asChild>
              <a href="/contact" onClick={() => setMobileMenuOpen(false)}>
                <MessageSquare className="h-4 w-4" />
                <span>{t('header.contactUs')}</span>
              </a>
            </Button>

            {/* Mobile Language Selector */}
            <div className="space-y-2">
              <p className="font-medium">{t('header.language')}</p>
              <div className="space-y-1 pl-4">
                {languages.map((language) => (
                  <Button
                    key={language.code}
                    variant="ghost"
                    className="block w-full justify-start"
                    onClick={() => {
                      handleLanguageChange(language.name);
                      setMobileMenuOpen(false);
                    }}
                  >
                    {language.name}
                  </Button>
                ))}
              </div>
            </div>

            {/* Mobile Theme Toggle */}
            <Button
              variant="ghost"
              onClick={toggleTheme}
              className="flex items-center space-x-2 w-full justify-start"
            >
              {theme === "dark" ? (
                <>
                  <Sun className="h-4 w-4" />
                  <span>{t('header.lightMode')}</span>
                </>
              ) : (
                <>
                  <Moon className="h-4 w-4" />
                  <span>{t('header.darkMode')}</span>
                </>
              )}
            </Button>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;