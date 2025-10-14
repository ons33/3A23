<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;
use App\Repository\AuthorRepository;
use Doctrine\Persistence\ManagerRegistry;
use App\Entity\Author;
final class AuthorController extends AbstractController
{
    #[Route('/author', name: 'app_author')]
    public function index(): Response
    {
        return $this->render('author/index.html.twig', [
            'controller_name' => 'AuthorController',
        ]);
    }

     #[Route('/get', name: 'get_author')]
    public function getAll(AuthorRepository $authRepo  ): Response
    {
        $authors = $authRepo->findAll();


        return $this->render('author/index.html.twig', [
            'authors' => $authors,
        ]);
    }

      #[Route('/add', name: 'add_author')]
    public function addAuth(ManagerRegistry $em): Response
    {
        $auth1= new Author();
        $auth1->setUsername('author1');
        $auth1->setEmail('author1@esprit.tn');

        $auth2= new Author();
        $auth2->setUsername('author2');
        $auth2->setEmail('author2@esprit.tn');

        $em->getManager()->persist($auth1);
        $em->getManager()->persist($auth2);
        $em->getManager()->flush();


        return New Response(' author added');
    }
     #[Route('/delete/{id}', name: 'app_delete')]
    public function deleteAuthor(ManagerRegistry $em,AuthorRepository $authRepo,$id): Response
    {
         
        $em->getManager()->remove($auth);
        $em->getManager()->flush();
       return New Response(' author deleted');
    }

}
