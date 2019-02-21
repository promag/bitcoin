// Copyright (c) 2019 The Bitcoin Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#include <qt/createwalletdialog.h>
#include <qt/forms/ui_createwalletdialog.h>

CreateWalletDialog::CreateWalletDialog(QWidget* parent)
    : QDialog(parent)
    , ui(new Ui::CreateWalletDialog)
{
    ui->setupUi(this);
}

CreateWalletDialog::~CreateWalletDialog()
{
    delete ui;
}

QString CreateWalletDialog::getWalletName() const
{
    return ui->wallet_name_line_edit->text();
}

bool CreateWalletDialog::isBlank() const
{
    return ui->blank_wallet_checkbox->isChecked();
}

bool CreateWalletDialog::isDisabledPrivateKeys() const
{
    return ui->disable_privkeys_checkbox->isChecked();
}

bool CreateWalletDialog::isEncrypt() const
{
    return ui->encrypt_wallet_checkbox->isChecked();
}

/*
    // Check that the wallet doesn't already exist
    if (m_wallet_controller->checkWalletExists(wallet_name)) {
        QMessageBox::critical(this, tr("Wallet creation failed"), tr("A wallet with the name <b>%1</b> already exists").arg(QString(wallet_name.c_str()).toHtmlEscaped()));
        QDialog::reject();
        return;
    }

    // Create the wallet
    std::unique_ptr<interfaces::Wallet> wallet = m_wallet_controller->createWallet(wallet_name, flags);

    if (wallet) {
        WalletModel* model = m_wallet_controller->getOrCreateWallet(std::move(wallet));
        // Encrypt the wallet
        m_parent->setCurrentWallet(model);
    } else {
        QMessageBox::critical(this, tr("Wallet creation failed"), tr("Wallet creation failed due to an internal error. The wallet was not created."));
    }
    dialog->hide();
    QDialog::accept();
}
*/
