import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, OneToMany } from 'typeorm';
import { Grabacion } from '../../../src/grabaciones/entities/grabacion.entity';

@Entity('usuarios')
export class Usuario {
  @PrimaryGeneratedColumn()
  id_usuario: number;

  @Column()
  nombre: string;

  @Column()
  email: string;

  @Column()
  contrasena_hash: string;

  @CreateDateColumn({ type: 'timestamp' })
  fecha_creacion: Date;

  @OneToMany(() => Grabacion, (grabacion) => grabacion.usuario)
  grabaciones: Grabacion[];
}
