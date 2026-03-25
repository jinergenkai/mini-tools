import { useTranslation } from "react-i18next";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";

const ContactUs = () => {
  const { t } = useTranslation();

  return (
    <div className="container mx-auto py-12 mt-16">
      {/* Hero Section */}
      <section className="text-center mb-12">
        <h1 className="text-4xl font-bold mb-4">{t("contact.title")}</h1>
        <p className="text-lg text-muted-foreground mb-8">{t("contact.subtitle")}</p>
      </section>

      {/* Contact Form and Info Cards */}
      <div className="grid md:grid-cols-2 gap-8">
        {/* Contact Form */}
        <Card>
          <CardHeader>
            <CardTitle>{t("contact.form.title")}</CardTitle>
            <CardDescription>{t("contact.form.description")}</CardDescription>
          </CardHeader>
          <CardContent>
            <form className="space-y-4">
              <div>
                <Input placeholder={t("contact.form.name")} />
              </div>
              <div>
                <Input type="email" placeholder={t("contact.form.email")} />
              </div>
              <div>
                <Input placeholder={t("contact.form.subject")} />
              </div>
              <div>
                <Textarea placeholder={t("contact.form.message")} className="min-h-[120px]" />
              </div>
              <Button className="w-full">{t("contact.form.submit")}</Button>
            </form>
          </CardContent>
        </Card>

        {/* Company Info */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>{t("contact.info.about")}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <p className="text-muted-foreground">
                  TMA Solutions is a leading software outsourcing company in Vietnam,
                  providing high-quality software services to global clients since 1997.
                </p>
                <Button variant="outline" className="w-full" asChild>
                  <a href="https://www.tmasolutions.vn" target="_blank" rel="noopener noreferrer">
                    {t("contact.info.visitWebsite")}
                  </a>
                </Button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>{t("contact.info.address")}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                TMA Innovation Park, Công viên Phần mềm Quang Trung,
                Tan Chanh Hiep Ward, District 12, Ho Chi Minh City, Vietnam
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>{t("contact.info.contact")}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <p className="text-muted-foreground">
                Email: contact@tma.com.vn
              </p>
              <p className="text-muted-foreground">
                Tel: (+84) 28 3997 8000
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default ContactUs;